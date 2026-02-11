import logging
from typing import List

from langchain_core.documents import Document
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

logger = logging.getLogger(__name__)


class Workflow:
    """
    This class represents a workflow for processing information retrieval tasks.
    It takes a set of tools and models and builds a state graph to execute them
    in a specific order based on the results of previous steps.

    Args:
        retriever (object): An object responsible for retrieving documents from a vector store.
        docs (list[Document], optional): A list of documents to process (used for summaries).
        Defaults to None.
        summary_chain (object): An object responsible for generating summaries of documents.
        rag_chain (object): An object responsible for generating answers using retrieved documents.
        retrieval_grader (object): An object responsible for grading the relevance of retrieved
        documents.
        hallucination_grader (object): An object responsible for checking if the generated answer
        is grounded in the documents.
        answer_grader (object): An object responsible for checking if the generated answer addresses
        the question.
        web_search_tool (object): An object responsible for searching the web for relevant
        information.
    """

    def __init__(
        self,
        retriever,
        docs,
        summary_chain,
        rag_chain,
        retrieval_grader,
        hallucination_grader,
        answer_grader,
        web_search_tool,
    ):
        self.retriever = retriever
        self.rag_chain = rag_chain
        self.retrieval_grader = retrieval_grader
        self.hallucination_grader = hallucination_grader
        self.answer_grader = answer_grader
        self.web_search_tool = web_search_tool
        self.docs = docs
        self.summary_chain = summary_chain
        # return self.build()

    def build(self):
        """
        Builds a state graph representing the workflow for processing information retrieval tasks.

        Returns:
            StateGraph: A compiled state graph object.
        """
        workflow = StateGraph(self.GraphState)
        workflow.add_node("websearch", self.web_search)
        workflow.add_node("retrieve", self.retrieve)
        workflow.add_node("grade_documents", self.grade_documents)
        workflow.add_node("generate", self.generate)
        workflow.add_node("summary", self.generate_summary)
        workflow.add_edge("summary", END)
        workflow.add_node("rag", self.init_rag)
        workflow.add_edge("rag", "retrieve")
        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            self.decide_to_generate,
            {
                "websearch": "websearch",
                "generate": "generate",
            },
        )
        workflow.add_edge("websearch", "generate")
        workflow.add_conditional_edges(
            "generate",
            self.grade_generation_v_documents_and_question,
            {
                "not supported": "generate",
                "useful": END,
                "not useful": "websearch",
            },
        )
        workflow.set_conditional_entry_point(
            self.route_chain,
            {
                "summary": "summary",
                "rag": "rag",
            },
        )
        return workflow.compile()

    class GraphState(TypedDict):
        """
        Represents the state of our graph.

        Attributes:
            question: question
            generation: LLM generation
            web_search: whether to add search
            documents: list of documents
            count: # of time generate step executed
        """

        question: str
        generation: str
        web_search: str
        documents: List[str]
        count: int
        retries: int

    ### Nodes
    def retrieve(self, state):
        """
        Retrieve documents from vectorstore

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        logger.info("---RETRIEVE---")
        question = state["question"]

        # Retrieval
        documents = self.retriever.invoke(question)
        return {
            "documents": documents,
            "question": question,
            "retries": state["retries"],
            "count": state["count"],
        }

    def init_rag(self, state):
        """
        Initialize the RAG chain

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Initialized elements to state
        """
        return state

    def generate(self, state):
        """
        Generate answer using RAG on retrieved documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        logger.info("---GENERATE---")
        question = state["question"]
        documents = state["documents"]
        count = 0 if state["count"] is None else (state["count"] + 1)
        # RAG generation
        generation = self.rag_chain.invoke({"context": documents, "question": question})
        return {
            "documents": documents,
            "question": question,
            "generation": generation,
            "count": count,
            "retries": state["retries"],
        }

    def generate_summary(self, _):
        """
        Generate summary of all documents using RAG on retrieved documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): generation, that contains LLM generation
        """
        logger.info("---SUMMARY---")
        return {"generation": self.summary_chain.run(self.docs)}

    def grade_documents(self, state):
        """
        Determines whether the retrieved documents are relevant to the question
        If any document is not relevant, we will set a flag to run web search

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Filtered out irrelevant documents and updated web_search state
        """

        logger.info("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        # Score each doc
        filtered_docs = []
        web_search = "No"
        for d in documents:
            score = self.retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            )
            grade = score["score"]
            # Document relevant
            if grade.lower() == "yes":
                logger.info("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            # Document not relevant
            else:
                logger.info("---GRADE: DOCUMENT NOT RELEVANT---")
                # We do not include the document in filtered_docs
                # We set a flag to indicate that we want to run web search
                web_search = "Yes"
                continue
        return {
            "documents": filtered_docs,
            "question": question,
            "web_search": web_search,
            "retries": state["retries"],
        }

    def web_search(self, state):
        """
        Web search based based on the question

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Appended web results to documents
        """

        logger.info("---WEB SEARCH---")
        question = state["question"]
        documents = state["documents"]

        # Web search
        docs = self.web_search_tool.invoke({"query": question})
        # Not needed in Google Search
        # docs = "\n".join([d["content"] for d in docs])
        web_results = Document(page_content=docs)
        if documents is not None:
            documents.append(web_results)
        else:
            documents = [web_results]
        return {
            "documents": documents,
            "question": question,
            "retries": state["retries"],
            "count": state["count"],
        }

    def route_chain(self, state):
        """
        Routes the workflow execution based on the current question in the state.

        This method checks the question in the state and determines the appropriate entry
        point for the workflow.
        If the question is "summary", the workflow execution starts at the "summary"
        node. Otherwise,
        it starts at the "rag" node.

        Args:
            state (GraphState): The current state of the workflow.

        Returns:
            str: The name of the node to start execution at ("summary" or "rag").
        """
        logger.info("---ROUTE CHAIN---")
        question = state["question"]
        if question == "summary":
            logger.info("---ROUTE QUESTION TO SUMMARY---")
            return "summary"
        else:
            logger.info("---ROUTE QUESTION TO RAG---")
            return "rag"

    def decide_to_generate(self, state):
        """
        Determines whether to generate an answer, or add web search

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """

        logger.info("---ASSESS GRADED DOCUMENTS---")
        web_search = state["web_search"]

        if web_search == "Yes":
            # All documents have been filtered check_relevance
            # We will re-generate a new query
            logger.info(
                "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
            )
            return "websearch"
        else:
            # We have relevant documents, so generate answer
            logger.info("---DECISION: GENERATE---")
            return "generate"

    ### Conditional edge
    def grade_generation_v_documents_and_question(self, state):
        """
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """

        logger.info("---CHECK HALLUCINATIONS---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]
        generation_count = state["count"]

        if generation_count > state["retries"]:
            logger.info("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"

        score = self.hallucination_grader.invoke(
            {"documents": documents, "generation": generation}
        )
        grade = score["score"]

        # Check hallucination
        if grade == "yes":
            logger.info("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
            # Check question-answering
            logger.info("---GRADE GENERATION vs QUESTION---")
            score = self.answer_grader.invoke(
                {"question": question, "generation": generation}
            )
            grade = score["score"]
            if grade == "yes":
                logger.info("---DECISION: GENERATION ADDRESSES QUESTION---")
                return "useful"
            else:
                logger.info("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
                return "not useful"
        else:
            if generation_count == state["retries"]:
                logger.info(
                    "---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, WEB SEARCH---"
                )
                return "not useful"
            logger.info(
                "---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---"
            )
            return "not supported"

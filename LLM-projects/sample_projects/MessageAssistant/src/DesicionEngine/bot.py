from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from .event_broker import VectorStoreManager, ContentRouterAssistant
from src.Tools.script_writer_agent import (press_release_prompt,
                                           client_brief_prompt,
                                           content_strategy_prompt,
                                           speech_writing,
                                           none_case_catcher)


class LLMQAInteraction:
    def __init__(self, openai_api_key,
                 stm_directory,
                 store_name,
                 table_name,
                 llm_model_name="gpt-3.5-turbo-0125",
                 temperature=0,
                 max_tokens=1000):

        self.NEW_DATA_KEYWORDS = {'explain', 'define', 'what is', 'how does', 'describe', 'details about'}
        self.FOLLOW_UP_INDICATORS = {'this mean', 'you said', 'further', 'more about', 'expand on', 'elaborate'}
        self.openai_api_key = openai_api_key
        self.stm_directory = stm_directory
        self.store_name = store_name
        self.table_name = table_name
        self.topic = None
        self.current_document = None
        self.chat_history = []
        self.context_payload = []
        self.llm = ChatOpenAI(model_name=llm_model_name,
                              temperature=temperature,
                              openai_api_key=openai_api_key,
                              max_tokens=max_tokens)  # gpt-4-0125-preview
        self._initialize_vector_store()
        self._setup_content_router()
        self._setup_prompt_templates()

    def _setup_content_router(self):
        self.content_router = ContentRouterAssistant(openai_api_key=self.openai_api_key)

    def _initialize_vector_store(self):
        print(self.stm_directory, self.store_name, self.table_name, self.openai_api_key)
        self.vectorstore_manager = VectorStoreManager(stm_directory=self.stm_directory,
                                                      store_name=self.store_name,
                                                      table_name=self.table_name,
                                                      openai_api_key=self.openai_api_key)
        # self.vectorstore_manager.create_index()
        self.vectorstore = self.vectorstore_manager.vectorstore

    def _setup_prompt_templates(self):
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
            which might reference context in the chat history, formulate a standalone question \
            which can be understood without the chat history. Do NOT answer the question, \
            just reformulate it if needed and otherwise return it as is."""

        self.contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])

        self.contextualize_q_chain = self.contextualize_q_prompt | self.llm | StrOutputParser()

        qa_system_prompt = """You are an assistant for question-answering tasks. \
            Use the following pieces of retrieved context to answer the question. \
            If you don't know the answer, just say that you don't know. \
            Use three sentences maximum and keep the answer concise.\

            {context}"""

        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])

    def _refactor_qa_prompt(self, question):
        routed_topic = self.content_router.process_input(question)
        print("SELECTED TOPIC: ", routed_topic.name)
        match routed_topic.name:
            case 'press-release':
                qa_system_prompt = press_release_prompt()
            case 'client-brief-clarification':
                qa_system_prompt = client_brief_prompt()
            case 'content-strategy-suggestion':
                qa_system_prompt = content_strategy_prompt()
            case 'speech-writing':
                qa_system_prompt = speech_writing()
            case _:
                qa_system_prompt = none_case_catcher()

        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])
        self.topic = routed_topic

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def ask_question(self, question):
        # Decide whether to re-retrieve data or use chat history
        need_new_data = self._decide_retrieval_based_on_question(question)

        contextualized_question = question  # Default to the original question
        if self.chat_history:
            # If there's relevant chat history and no need for new data, use the chat history
            contextualized_question = self.contextualize_q_chain.invoke({
                "chat_history": self.chat_history,
                "question": question,
            })

        # If the chat history is empty or the topic has changed, update the QA prompt
        if self.chat_history is None or self.topic != self.content_router.process_input(question):
            self._refactor_qa_prompt(question)

        # Update the chat history with the new question
        self.chat_history.append(HumanMessage(content=question))

        formatted_docs = ""
        if need_new_data:
            # Retrieve relevant documents based on the contextualized question
            retrieved_docs = self.vectorstore.similarity_search(contextualized_question)
            self.current_document = retrieved_docs
            formatted_docs = self._format_docs(retrieved_docs)

        # Use the retrieved context and/or chat history to answer the question
        answer = (self.qa_prompt | self.llm).invoke({
            "chat_history": self.chat_history,
            "question": contextualized_question,
            "document": formatted_docs,
        })

        # Update the chat history with the AI's answer
        self.chat_history.append(answer)
        self.context_payload.append({"question": question,
                                     "documents": formatted_docs})

        return answer

    def _decide_retrieval_based_on_question(self, question):
        question_lower = question.lower()

        # Check for new data keywords
        if any(keyword in question_lower for keyword in self.NEW_DATA_KEYWORDS):
            return True
        # Check for follow-up indicators
        elif any(indicator in question_lower for indicator in self.FOLLOW_UP_INDICATORS):
            if self._is_related_to_chat_history(question_lower):
                return False  # Use existing chat history
        elif self.topic != self.content_router.process_input(question):
            return True

        retrieved_docs = self.vectorstore.similarity_search(question_lower)
        if retrieved_docs != self.current_document:
            self.current_document = retrieved_docs
            return True

        return True  # Default to fetching new data

    def _is_related_to_chat_history(self, question):
        significant_words = set(question.split())
        # Consider caching these combined texts if chat history and context_payload don't change often
        recent_history = " ".join(msg.content for msg in self.chat_history[-3:]).lower()
        retrieved_docs = " ".join(doc['document'] for doc in self.context_payload[-3:]).lower()

        combined_text = f"{recent_history} {retrieved_docs}"
        # Use efficient search (e.g., Aho-Corasick algorithm) if performance is critical
        return any(word in combined_text for word in significant_words)

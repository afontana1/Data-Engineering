import os
import lancedb
from langchain_community.vectorstores import LanceDB
from langchain_openai.embeddings import OpenAIEmbeddings
from semantic_router.encoders import OpenAIEncoder
from semantic_router import Route
from semantic_router.layer import RouteLayer


class VectorStoreManager:
    def __init__(self, stm_directory, store_name, table_name, openai_api_key):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.stm_dir = stm_directory
        self.store_name = store_name
        self.table_name = table_name
        self.db = self._connect_to_db()
        self.table = self._open_table()
        self.vectorstore = LanceDB(self.table, self.embeddings)

    def _connect_to_db(self):
        db_path = os.path.join(self.stm_dir, self.store_name)
        return lancedb.connect(str(db_path))

    def _open_table(self):
        return self.db.open_table(self.table_name)

    def create_index(self, metric="cosine", vector_column_name="vector", num_partitions=256, num_sub_vectors=96):
        self.table.create_index(metric=metric, vector_column_name=vector_column_name,
                                num_partitions=num_partitions, num_sub_vectors=num_sub_vectors)

    def similarity_search(self, query, k=3):
        return self.vectorstore.similarity_search(query, k=k)


class ContentRouterAssistant:
    def __init__(self, openai_api_key):
        self.routes = []
        self.encoder = OpenAIEncoder(openai_api_key=openai_api_key)
        self._initialize_routes()

    def _initialize_routes(self):
        press_release = Route(
            name="press-release",
            utterances=[
                "is the tone of this press release appropriate for our target media outlets?",
                "summarize the key points of this press release",
                "what is the sentiment of this PR's content?",
                "check for any grammatical or factual errors in this press release",
                "identify the primary message and target audience of this press release",
                "what are the key products or services introduced in this press release?",
                "does the press release mention any upcoming events or launches?",
                "can you identify any specific target markets or audiences the press release is addressing?",
                "what are the plans or directions outlined in the press release for the company or its products/services"
            ],
        )

        client_brief = Route(
            name="client-brief-clarification",
            utterances=[
                "can you help me understand the primary goals of this campaign as outlined in their brief?",
                "who is the target audience for this campaign, according to the client brief",
                "what are the main messages we need to communicate in this campaign?",
                "based on the client brief, which media outlets should we prioritize?",
                "are there any specific media outlets mentioned in the client brief that we should focus on for outreach?",
                "what strategic approach is suggested in the client brief for achieving the campaign objectives?",
                "what tone and style of content does the client brief recommend for engaging the target demographic?",
                "does the client brief mention any competitors, and how does client want to differentiate from them?",
                "what are the key performance indicators (KPIs) outlined in the client brief for the campaign?"
            ],
        )

        client_strategy = Route(
            name="strategy-suggestion",
            utterances=[
                "can you analyze the trends in our past content to suggest themes for the given time-frame?",
                "what are the emerging topics in our industry that we haven't covered yet?",
                "how can we align our content strategy with the latest research findings?",
                "hold brainstorming sessions to translate research insights into strategic content ideas",
                "can you recommend content ideas that would fill the gaps in our current coverage?",
                "how can we diversify our content to reach a broader audience in the given time-frame?",
                "create a pilot project to test new content formats and measure audience engagement",
                "are there any industry events or milestones coming up that we should focus our content around?",
                "identify upcoming industry events, milestones, or seasonal topics that should be the content strategy"
            ],
        )

        speech_writing = Route(
            name="speech-writing",
            utterances=[
                "craft a narrative for our upcoming keynote address that aligns corporate vision and strategic goals"
                "can you develop a speech for our COO that showcases leadership and foresight?",
                "I need expertise to devise a presentation that underscores our innovations and trajectory",
                "draft an inspiring and motivational address that energizes and aligns with our initiatives?",
                "create a speech that highlights our commitment to responsibility and engagement?",
                "require a persuasive and data-driven speech to present, outlining financial health and growth",
                "formulate a transparent and reassuring speech to reinforce trust and confidence",
                "synthesize a visionary speech that positions us as thought leaders and pioneers in our industry",
                "need a speech that articulates our strategy and commitment to markets, resonating with a diverse audience"
            ],
        )

        self.routes.extend([press_release, client_brief, client_strategy, speech_writing])

    def process_input(self, input_text):
        rl = RouteLayer(encoder=self.encoder, routes=self.routes)
        return rl(input_text)

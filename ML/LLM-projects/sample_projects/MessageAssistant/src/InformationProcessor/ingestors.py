import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from .preprocessor import call_pdf_preprocess, call_image_preprocess, call_audio_preprocess
from .utils.semantic_chuncker import SemanticChunker
from .utils.txt_preprocessor import NERExtractor
from langchain_openai.embeddings import OpenAIEmbeddings
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector
import lancedb
import uuid
from time import sleep
import colorama

registry = EmbeddingFunctionRegistry().get_instance()
openai = registry.get("openai").create()


class Schema(LanceModel):
    vector: Vector(openai.ndims()) = openai.VectorField()
    id: str
    text: str


@dataclass
class SrcType:
    txt: List[str] = field(default_factory=lambda: ['txt', 'csv', 'json'])
    pdf: List[str] = field(default_factory=lambda: ['pdf'])
    word: List[str] = field(default_factory=lambda: ['doc', 'docx'])
    image: List[str] = field(default_factory=lambda: ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'])
    sound: List[str] = field(default_factory=lambda: ['mp3', 'wav', 'aac', 'flac', 'ogg'])


class SrcIngestor(SrcType, NERExtractor):
    """
    class that will read any document or file of various format and store its content in the corresponding memory bank
    """
    def __init__(self, memory_bank: str,
                 sess_name: str,
                 file_sources: Dict[str, list[str]],
                 schema=Schema,
                 openai_api=None) -> None:
        super().__init__()
        NERExtractor.__init__(self)
        self.entities = None
        self.ai_credentials = openai_api
        self.base_schema = schema
        self.memory_bank = memory_bank
        self.file_sources = file_sources
        self._embeddings = OpenAIEmbeddings(openai_api_key=self.ai_credentials)
        current_dir = os.path.dirname(__file__)
        stm_dir = os.path.join(current_dir, '..', 'STM')
        self.db = lancedb.connect(f"{stm_dir}\\{self.memory_bank}")
        self._table = self.db.create_table(f"{sess_name}", schema=self.base_schema, mode="overwrite")

    def file_broker(self, progress_update=None) -> None:
        """
        This function will take file_sources and pair it with the corresponding method to ingest the file.
        """
        for file_type, files in self.file_sources.items():
            for file in files:
                extension = file.split('.')[-1]
                if extension in self.txt:
                    self.ingest_txt(file)
                elif extension in self.pdf:
                    # print in blue color
                    print(colorama.Fore.BLUE + f"Processing PDF {file}...")
                    sleep(2)
                    self.ingest_pdf(file, open_ai=self.ai_credentials)
                elif extension in self.word:
                    self.ingest_word(file)
                elif extension in self.image:
                    # print in blue color
                    print(colorama.Fore.BLUE + f"Processing Image {file}...")
                    sleep(2)
                    self.ingest_image(file, open_ai=self.ai_credentials)
                elif extension in self.sound:
                    # print in blue color
                    print(colorama.Fore.BLUE + f"Processing Audio file {file}...")
                    sleep(2)
                    self.ingest_sound(file)
                else:
                    print(f"Unsupported file type: {file}")

                os.remove(file)

    def add_text(self, texts: List[Any], metadata: Optional[List[dict]] = None) -> None:
        docs = []
        ids = [str(uuid.uuid4()) for _ in texts]
        embeddings = self._embeddings.embed_documents(texts)
        for idx, text in enumerate(texts):
            embedding = embeddings[idx]
            meta = metadata[idx] if metadata else {}
            # make a string out of metadata
            str_meta = '[DOCUMENT INFO]:\n' + ' '.join([f"{k}: {v}\n" for k, v in meta.items()]) if meta else ''
            entities = self.entities if self.entities else ''
            text += '\n' + str_meta + '\n' + entities
            docs.append(
                {
                    "vector": embedding,
                    "id": ids[idx],
                    "text": text,
                    **meta,
                }
            )
        self._table.add(docs)

    def store_data(self, documents, metadata) -> None:
        self.add_text(documents, metadata)

    def entity_finder(self, text):
        # Apply the bert-base-NER pipeline to the text
        self.entities = self.extract_entities(text)

    def ingest_word(self, payload) -> None:
        """
        This function will ingest a Word file and store its content in the corresponding memory bank.
        """
        pass

    def ingest_txt(self, payload) -> None:
        """
        This function will ingest a txt file (text, csv, json) and store its content in the corresponding memory bank.
        """
        pass

    def ingest_pdf(self, payload, open_ai) -> None:
        """
        This function will ingest a pdf file and store its content in the corresponding memory bank.
        """
        processed_pdf, size = call_pdf_preprocess(payload, open_ai)
        self.entity_finder(processed_pdf)
        txt_splitter, metadata = self.chunker(payload, processed_pdf, size, 'pdf')
        pdf_documents = txt_splitter.split_text(processed_pdf)
        self.store_data(pdf_documents, metadata)

    def ingest_image(self, payload, open_ai) -> None:
        """
        This function will ingest an image file and store its content in the corresponding memory bank.
        """
        processed_image, metadata = call_image_preprocess(payload, open_ai)
        txt_splitter, metadata = self.chunker(payload, processed_image, metadata, 'image')
        image_documents = txt_splitter.split_text(processed_image)
        self.store_data(image_documents, metadata)

    def ingest_sound(self, payload) -> None:
        """
        This function will ingest a sound file and store its content in the corresponding memory bank.
        """
        preprocessed_audio, metadata = call_audio_preprocess(payload)
        txt_splitter, metadata = self.chunker(payload, preprocessed_audio, metadata, 'sound')
        audio_documents = txt_splitter.split_text(preprocessed_audio)
        self.store_data(audio_documents, metadata)

    def chunker(self, payload, preprocessed_file, metadata, action):
        """
        This function will chunk the audio file into smaller pieces and store its content in the corresponding memory bank.
        """
        file_name = os.path.basename(payload).split('.')[0]
        text_splitter = SemanticChunker(self._embeddings)
        other_file_names = os.listdir(payload.split(file_name)[0])
        metadata_dic = [{'file_name': file_name, 'other_files': other_file_names,
                         'doc_info': {'file_type': action, 'metadata': metadata}}
                        for _ in range(len(preprocessed_file))]
        return text_splitter, metadata_dic

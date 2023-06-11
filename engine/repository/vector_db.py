import uuid
import chromadb

from typing import List
from chromadb.config import Settings

class EmbeddingStorage:

    def __init__(self) -> None:
        # TODO: set up remote communication with this; possibly rewrite to be async
        self.client = chromadb.Client(Settings(chroma_api_impl="rest",
                                        chroma_server_host="localhost",
                                        chroma_server_http_port="8000"
                                    ))

    def add_image_embedding(self, client: str, img_id: str, img_embedding: List[float]) -> None:
        collection = self.client.get_or_create_collection(name=client)
        collection.add(
            documents=[img_id],
            embeddings=[img_embedding],
            ids=[img_id]
        )

    def query(self, client: str, embedding: List[float], n: int = 3):
        collection = self.client.get_or_create_collection(name=client)
        res = collection.query(
            query_embeddings=[embedding],
            n_results=n,
        )

        return res

storage = EmbeddingStorage()

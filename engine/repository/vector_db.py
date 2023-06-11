import uuid
import chromadb

from typing import List

class EmbeddingStorage:

    def __init__(self) -> None:
        # TODO: set up remote communication with this; possibly rewrite to be async
        self.client = chromadb.Client()

    def __get_str_uuid(self):
        return str(uuid.uuid4())

    def add_image_embedding(self, client: str, img_id: str, img_embedding: List[float]) -> None:
        collection = self.client.get_or_create_collection(name=client)
        collection.add(
            documents=[img_id],
            embeddings=[img_embedding],
            ids=[self.__get_str_uuid()] # TODO: this is not data specific
        )

    def query(self, client: str, embedding: List[float], n: int = 3):
        collection = self.client.get_or_create_collection(name=client)
        res = collection.query(
            query_embeddings=[embedding],
            n_results=n,
            # where={
            #     "name": {
            #         "$eq": "user1"
            #     }
            # }
        )

        return res

storage = EmbeddingStorage()
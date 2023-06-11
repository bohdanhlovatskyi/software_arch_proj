import chromadb
import numpy as np
from chromadb.config import Settings

# client = chromadb.Client(Settings(
#     # chroma_api_impl="rest",
#     # chroma_server_host="localhost",
#     # chroma_server_http_port="8000",
#     chroma_db_impl="duckdb+parquet",
#     # persist_directory="vectors" # Optional, defaults to .chromadb/ in the current directory
# ))

client = chromadb.Client()

collection = client.create_collection(
        name="user1",
        metadata={"hnsw:space": "cosine"}
)

if __name__ == "__main__":
    import pickle

    with open("cat_emb.pkl", "rb") as h:
        cat_emb = list(map(float, pickle.load(h)[0].astype(np.float32)))

    with open("dog_emb.pkl", "rb") as h:
        dog_emb = list(map(float, pickle.load(h)[0].astype(np.float32)))

    with open("text_emb.pkl", "rb") as h:
        text_emb = list(map(float, pickle.load(h)[0].numpy().astype(np.float32)))

    collection.add(
        documents=["cat"],
        embeddings=[cat_emb],
        ids=["id1"]
    )

    collection.add(
        documents=["dog"],
        embeddings=[dog_emb],
        ids=["id2"]
    )

    res = collection.query(
        query_embeddings=[text_emb],
        n_results=1,
        # where={
        #     "name": {
        #         "$eq": "user1"
        #     }
        # }
    )


    print(res)

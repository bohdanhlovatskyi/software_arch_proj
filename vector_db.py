import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    # chroma_api_impl="rest",
    # chroma_server_host="localhost",
    # chroma_server_http_port="8000",
    chroma_db_impl="duckdb+parquet",
    # persist_directory="vectors" # Optional, defaults to .chromadb/ in the current directory
))

collection = client.create_collection(
        name="user1",
        metadata={"hnsw:space": "cosine"}
)

if __name__ == "__main__":
    import pickle

    with open("cat_emb.pkl", "rb") as h:
        cat_emb = pickle.load(h)

    with open("dog_emb.pkl", "rb") as h:
        dog_emb = pickle.load(h)

    with open("text_emb.pkl", "rb") as h:
        text_emb = pickle.load(h)

    collection.add(
        documents=["cat", "dog"],
        embeddings=[cat_emb, dog_emb],
        ids=["id1", "id2"]
    )

    res = collection.query(
        query_embeddings=text_emb,
        n_results=1,
        # where={
        #     "name": {
        #         "$eq": "user1"
        #     }
        # }
    )


    print(res)

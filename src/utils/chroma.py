import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
import json
import hashlib

load_dotenv()
environment = os.getenv("ENVIRONMENT")

if environment == "DEV":
    database_path = "database.jsonl"
else:
    database_path = "/app/data/database.jsonl"

class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")
        
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = self.model.encode(input).tolist()
        return embeddings

class ChromaClient:
    def __init__(self):
        self.client = chromadb.EphemeralClient()
        self.documents: list[str] = []



        self.collection = self.client.get_or_create_collection(
            name="glados_memory",
            embedding_function=MyEmbeddingFunction(),
            configuration= {
                "hnsw": {
                    "space": "cosine"
                }
            }
        )

        self.load()
    

    def load(self):
        self.documents.clear()

        with open(database_path, 'r') as f:
            data = [json.loads(line) for line in f]
        
        for document in data:
            self.documents.append(document["info"])

        if not self.documents:
            return
        
        self.collection.upsert(
            ids=[hashlib.md5(document.encode()).hexdigest() for document in self.documents],
            documents=self.documents
        )

    
    def query(self, text: list[str], n_results: int) -> tuple[str, float]:
        results = self.collection.query(query_texts=text, n_results=n_results)

        document = results["documents"][0][0]
        distance = results["distances"][0][0]
        return document, distance


    def add(self, text: str):
        if not os.path.exists(database_path):
            f = open(database_path, "w")
            f.close()
        
        with open(database_path, "a") as f:
            document = {
                "info": text
            }
            f.write(json.dumps(document) + "\n")
        
chroma_client = ChromaClient()
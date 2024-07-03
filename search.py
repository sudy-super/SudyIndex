import json
import numpy as np
import time
import os
from embedding_model import CreateEmbedding

class SearchFromIndex:
    def __init__(self):
        # self.index = json.load(open(index_path))
        # self.node_data = json.load(open(node_path))
        # self.embedding_data = json.load(open(embedding_path))

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.node_path = os.path.join(script_directory, "node_store.json")
        self.embedding_path = os.path.join(script_directory, "embedding_store.json")

        print("[CHECKPOINT] SearchFromIndex System Startup!")

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def query(self, query_str, top_k, cutoff=None):

        with open(self.node_path, "r", encoding="utf-8") as node_f:
            node_data = json.load(node_f)
        with open(self.embedding_path, "r", encoding="utf-8") as embedding_f:
            embedding_data = json.load(embedding_f)

        # クエリを埋め込みに変換
        embedding = self.get_embedding(query_str)

        similarities = []
        for node_id, compared_embedding in embedding_data['embedding_dict'].items():
            # ノードに対応した埋め込みデータを取得
            compared_embedding = compared_embedding

            # 対応するnodeIDを取得
            corresponding_id = node_data['nodestore/data'][node_id]['__data__']['node_id']

            # 類似度を計算
            similarity = self.cosine_similarity(embedding, compared_embedding)
            if cutoff and similarity < cutoff:
                continue

            similarities.append({"similarity": similarity, "id": corresponding_id})

        # ソートしてtop_kを返す
        similarities.sort(key=lambda o: o["similarity"], reverse=True)
        print("[CHECKPOINT] Return Similarities List!")
        return similarities[:top_k]

    def get_embedding(self, text):
        embedding_instance = CreateEmbedding()
        return embedding_instance.creating_embedding(text)

if __name__ == "__main__":
    # インデックス、ノードデータ、埋め込みデータのファイルパスを指定してSearchFromIndexを作成
    # index_path = 'index_store.json'
    node_path = 'node_store.json'
    embedding_path = 'embedding_store.json'
    index = SearchFromIndex(node_path, embedding_path)

    # クエリを指定して検索
    query_input = input("クエリ:")
    query = [query_input]
    results = index.query(query, top_k=10, cutoff=0.1)

    elapsed = int((time.time() - start) * 1000)
    
    # 結果を表示
    for result in results:
        print(result["similarity"], result["sentence"])
    print(f"Elapsed: {elapsed}ms")
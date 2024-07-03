import json
import os
import settings
from datetime import datetime

class Calculation:
    def __init__(self):
        # self.index = SearchFromIndex(node_path, embedding_path)

        # パラメータ
        self.k = settings.retrieve_number_rate  # 上位k個を取得する

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.index_store_path = os.path.join(script_directory, 'index_store.json')
        self.node_path = os.path.join(script_directory, 'node_store.json')
        self.embedding_path = os.path.join(script_directory, 'embedding_store.json')
        
        print("[CHECKPOINT] Calculation Of Similarlity System Startup!")

    def processing_info(self, results):
        # results = self.index.query(query, top_k=10, cutoff=0.3)

        # インデックスデータの読み込み
        with open(self.index_store_path, "r", encoding="utf-8") as file:
            index_data = json.load(file)

        # ノードデータの読み込み
        with open(self.node_path, "r", encoding="utf-8") as file:
            node_data = json.load(file)

        # ノードIDと類似度の対応を作成
        similarity_dict = {data["id"]: data["similarity"] for data in results}

        # ノードの情報を取得して加工
        node_info_list = []
        for node_id, similarity in similarity_dict.items():
            if node_id in node_data["nodestore/data"]:
                node_info = node_data["nodestore/data"][node_id]["__data__"]
                made_time = node_info["meta_data"]["made_time"]
                last_accessed_time = node_info["meta_data"]["last_accessed_time"]
                node_length = node_info["node_info"]["node_length"]

                # 現在の時刻との差を計算
                current_time = datetime.now()
                made_time_diff = current_time - datetime.strptime(made_time, "%Y-%m-%d %H:%M:%S")
                last_accessed_time_diff = current_time - datetime.strptime(last_accessed_time, "%Y-%m-%d %H:%M:%S")

                # 時間差を時間単位に変換
                made_time_diff_hours = made_time_diff.total_seconds() / 3600
                last_accessed_time_diff_hours = last_accessed_time_diff.total_seconds() / 3600

                node_info_list.append(
                    {
                        "node_id": node_id,
                        "similarity": similarity,
                        "made_time_diff": made_time_diff_hours,
                        "last_accessed_time_diff": last_accessed_time_diff_hours,
                        "node_length": node_length
                    }
                )

        # 類似度に忘却関数x=1/(0.02x+1)を適用
        for node_info in node_info_list:
           x = node_info["last_accessed_time_diff"]
           node_info["similarity"] *= 1 / (settings.forgetting_rate * x + 1)

        # 類似度でソートして上位k個を取得
        sorted_nodes = sorted(node_info_list, key=lambda x: x["similarity"], reverse=True)[:self.k]

        # ノードに対応するテキストを取得
        text_list = []
        for node in sorted_nodes:
            node_id = node["node_id"]
            if node_id in index_data["index_store/data"]["__data__"]["nodes_dict"]:
                text = node_data["nodestore/data"][node_id]["__data__"]["node"]
                text = made_time + "\n" + text
                text_list.append(text)
        text_string = ""
        for a_text in text_list:
            text_string += a_text + "\n\n"
        print("[CHECKPOINT] Calculated Similarlity and Made Memory Context!")
        return text_string

if __name__ == "__main__":

    cal_instance = Calculation()
    cal_result = cal_instance.processing_info(word)

    # 結果の出力
    for text in cal_result:
        print(text)
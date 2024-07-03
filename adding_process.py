import numpy as np
import json
from datetime import datetime
import csv
import os
import openai
from embedding_model import CreateEmbedding
from conversation_summ import CreateSummary

class AddingIndex:
    def __init__(self):
        self.crsumm = CreateSummary()
        self.embedding_instance = CreateEmbedding()

        script_directory = os.path.dirname(os.path.abspath(__file__))

        self.index_store_path = os.path.join(script_directory, "index_store.json")
        self.node_path = os.path.join(script_directory, 'node_store.json')
        self.embedding_path = os.path.join(script_directory, 'embedding_store.json')

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_embedding(self, text):
        return self.embedding_instance.creating_embedding(text)

    def generate_node_id(self, node_count):
        node_id = "node-{0:04d}-{1:04d}-{2:04d}-{3:04d}-{4:04d}".format(
            (node_count // 10000**4)%10000,
            (node_count // 10000**3)%10000,
            (node_count // 10000**2)%10000,
            (node_count // 10000)%10000,
            (node_count % 10000)
        )
        return node_id

    def add_index(self, stored_string):
        if (not os.path.exists(self.index_store_path)) or (os.path.getsize(self.index_store_path) == 0):
            index_data = {
                "index_store/data": {
                    "__data__": {
                        "nodes_dict": {
                        }
                    }
                }
            }
            node_count = 1
        else:
            # Load existing data from index_store.json
            with open(self.index_store_path, "r", encoding="utf-8") as index_file:
                try:
                    index_data = json.load(index_file)
                except json.JSONDecodeError as e:
                    print(f"Error: Could not decode JSON from file {self.index_store_path}. Error details: {e}")

            # Generate a new node ID
            node_count = len(index_data["index_store/data"]["__data__"]["nodes_dict"]) + 1

        new_node_id = self.generate_node_id(node_count)

        # Update index_store.json
        index_data["index_store/data"]["__data__"]["nodes_dict"][new_node_id] = new_node_id
        with open(self.index_store_path, "w", encoding="utf-8") as index_file:
            json.dump(index_data, index_file, indent=4)

        # Create data for node_store.json
        """
        node_data = {
            "nodestore/data": {
                new_node_id: {
                    "__data__": {
                        "node": stored_string,
                        "node_id": new_node_id,
                        "meta_data": {
                            "made_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "last_accessed_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        },
                        "node_info": {
                            "node_length": len(stored_string)
                        }
                    }
                }
            }
        }
        """

        if (not os.path.exists(self.node_path)) or (os.path.getsize(self.node_path) == 0):
            node_data_existing = {
                "nodestore/data": {
                }
            }
        else:
            with open(self.node_path, "r", encoding="utf-8") as node_file:
                try:
                    node_data_existing = json.load(node_file)
                except json.JSONDecodeError as e:
                        print(f"Error: Could not decode JSON from file {self.node_path}. Error details: {e}")

        node_data_existing["nodestore/data"][new_node_id] = {
            "__data__": {
                "node": "",
                "node_id": "",
                "meta_data": {
                    "made_time": "",
                    "last_accessed_time": ""
                },
                "node_info": {
                    "node_length": 0
                }
            }
        }

        node_data_existing["nodestore/data"][new_node_id]["__data__"]["node"] = stored_string
        node_data_existing["nodestore/data"][new_node_id]["__data__"]["node_id"] = new_node_id
        node_data_existing["nodestore/data"][new_node_id]["__data__"]["meta_data"]["made_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node_data_existing["nodestore/data"][new_node_id]["__data__"]["meta_data"]["last_accessed_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        node_data_existing["nodestore/data"][new_node_id]["__data__"]["node_info"]["node_length"] = len(stored_string)

        with open(self.node_path, "w", encoding="utf-8") as node_file:
            json.dump(node_data_existing, node_file, indent=4)

        if (not os.path.exists(self.embedding_path)) or (os.path.getsize(self.node_path) == 0):
            embedding_data = {
                "embedding_dict": {
                }
            }
        else:
            with open(self.embedding_path, "r", encoding="utf-8") as embedding_file:
                try:
                    embedding_data = json.load(embedding_file)
                except json.JSONDecodeError as e:
                        print(f"Error: Could not decode JSON from file {self.node_path}. Error details: {e}")

        # Get embedding for the stored string (dummy implementation)
        embedding = self.get_embedding(stored_string)
        embedding = embedding.tolist()

        # Update embedding_store.json
        embedding_data["embedding_dict"][new_node_id] = embedding
        with open(self.embedding_path, "w", encoding="utf-8") as embedding_file:
            json.dump(embedding_data, embedding_file, indent=4)

    def get_summ_gpt(self, conversation):
        return self.crsumm.get_summ_gpt(conversation)

    def load_string_store(self):
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            store1_path = os.path.join(script_directory, "string_store.txt")
            with open(store1_path, 'r', encoding="utf-8") as file:
                stored_string = file.read()
        except FileNotFoundError:
            stored_string = ""
        
        return stored_string

    def load_string_store_person(self):
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            store2_path = os.path.join(script_directory, "string_store_person.txt")
            with open(store2_path, 'r', encoding="utf-8") as file:
                stored_string_person = file.read()
        except FileNotFoundError:
            stored_string_person = ""
        
        return stored_string_person

    def process_string(self, person, string):
        stored_string = self.load_string_store()
        stored_string_person = self.load_string_store_person()
        string_embedding = self.get_embedding(string)
        stored_string_embedding = self.get_embedding(stored_string)
        similarity = self.cosine_similarity(string_embedding, stored_string_embedding)
        
        if similarity > 0.4:
            stored_string += "\n"
            stored_string += string
            stored_string_person += "\n"
            stored_string_person += person + ":" + string
        else:
            summ = self.get_summ_gpt(stored_string_person)
            self.add_index(summ)
            sentence = [stored_string_person, summ]
            script_directory = os.path.dirname(os.path.abspath(__file__))
            summ_study_path = os.path.join(script_directory, "conversation_summ_study.csv")
            with open(summ_study_path, "a", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(sentence)
            stored_string = ""
            stored_string += string
            stored_string_person = ""
            stored_string_person += f"{person}:{string}"
        
        script_directory = os.path.dirname(os.path.abspath(__file__))
        store1_path = os.path.join(script_directory, "string_store.txt")
        store2_path = os.path.join(script_directory, "string_store_person.txt")

        with open(store1_path, 'w', encoding="utf-8") as file:
            file.write(stored_string)
        with open(store2_path, 'w', encoding="utf-8") as file:
            file.write(stored_string_person)
        
        # return stored_string

if __name__ == "__main__":
    # 例として、文字列"example string"を処理する
    string = "example string"
    stored_string = self.load_string_store()
    updated_string = process_string(string, stored_string)
    print(updated_string)
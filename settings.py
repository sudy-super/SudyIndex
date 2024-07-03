import os
import json

# 現在のスクリプトのディレクトリを取得
script_directory = os.path.dirname(os.path.abspath(__file__))

# settings.jsonファイルへの相対パスを作成
settings_path = os.path.join(script_directory, "settings.json")

with open(settings_path, "r", encoding="utf-8") as node_f:
    settings_data = json.load(node_f)

settings_api_key = os.environ["OPENAI_API_KEY"]
settings_character_name = settings_data['character_name']
settings_listener_name = settings_data['listener_name']
setting_remember_rate = settings_data["remember_rate"]
setting_forgetting_rate = settings_data["forgetting_rate"]
setting_retrieve_number_rate = settings_data["retrieve_number_rate"]

openai_api_key_set = settings_api_key
character_name_set = settings_character_name
listener_name_set = settings_listener_name
remember_rate = setting_remember_rate
forgetting_rate = setting_forgetting_rate
retrieve_number_rate = setting_retrieve_number_rate
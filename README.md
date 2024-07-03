# SudyIndex

## 使い方


前提: OPENAI_API_KEYという環境変数にOpenAI APIキーが設定されていること。

### 1. settings.jsonを開いて以下の設定をします。

character_name: 応答システム側の名前を設定できます。

lisner_name: ユーザー側の名前を設定できます。

remember_rate: 想起時の類似度検索の閾値です。デフォルトは0.3で、数字を増やすとより関連度が高い記憶を抽出でき、減らすと比較的まんべんなく抽出できます。0.2から0.4がおすすめです。

forgetting_rate: 忘却度を制御する係数です。デフォルトは0.02で、数字を増やすと忘れやすく、減らすと忘れにくくなります。0.01から0.1がおすすめです。

retrieve_number_rate: データベースから取りだす記憶の数を制御できます。デフォルトは10です。

embedding_mode: local/gptでベクトル化をローカルでするかOpenAIのembedding-ada-002でするかを選べます。切り替えは未実装で、localで固定されています。

summary_mode: local/gptで要約をローカルでするかchatGPTでするかを選べます。切り替えは未実装で、gptで固定されています。


### 2. 以下のコードで動作させます。コードは例です。

```python
from sudy_index import SudyIndex

def __init__(self):
    self.memory_system = SudyIndex()
def system(self, userComment):
    calc_result = self.memory_system.system_running(userComment)
    ### ここに応答生成処理 ###
    aituber_response = # 応答
    self.memory_system.system_running2(aituber_response)
```

記憶システムを一つのフォルダにまとめた場合は下記のようにしてください。

```python
from <フォルダ名>.sudy_index import SudyIndex

def __init__(self):
    self.memory_system = SudyIndex()
def system(self, userComment):
    calc_result = self.memory_system.system_running(userComment)
    ### ここに応答生成処理 ###
    aituber_response = # 応答
    self.memory_system.system_running2(aituber_response)
```


calc_resultには

```
該当記憶の作成日時1
該当記憶の内容1

該当記憶の作成日時2
該当記憶の内容2
```

という形式で取り出された記憶情報が入っています。具体的には下記のようになります。

```
2023-06-14 02:56:59
リスナーが富士山の標高を尋ね、レイナは「634m」と間違った答えを返したが、リスナーに修正されて正しい答えは「3776m」であることが分かった。レイナ は自分の間違いを認めた。

2023-06-14 02:59:32
リスナーが「マリオの映画は観ましたか？」と尋ね、レイナは「観てない」と回答しました。
```

このままchatGPTのコンテキスト等に入れることが可能です。
また別途、conversation_history.csvから会話履歴を取り出すことも可能です(抽出コードは付属していません)。

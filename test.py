from sudy_index import SudyIndex

class test:
    def __init__(self):
        self.memory_system = SudyIndex()

    def system(self, userComment, aituber_response):
        calc_result = self.memory_system.system_running(userComment)
        print("========")
        print(calc_result)
        print("========")
        self.memory_system.system_running2(aituber_response)

if __name__ == '__main__':
    myText = ["こんにちは","今日は何をしていましたか？","良いですね。ところで、マリオの映画は観ましたか？", "富士山の標高は？", "違います、3776mです。", "そうですか、あなたの視力はいくつですか？", "すごい！私は0.5です。", "富士山の標高は？"]
    aiText = ["こんにちは","サッカーをしてた！","観てない", "634m！", "間違っちゃった、残念！", "私の視力は2.0！エスキモーと張り合えるよ！", "4倍じゃん！", "3776m！"]
    testinstance = test()
    for i in range(len(myText)):
        testinstance.system(myText[i],aiText[i])
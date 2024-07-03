import csv
import os

class CreateHistory:
    def make_history(self, person, inputs):
        sentence = [person, inputs]
        script_directory = os.path.dirname(os.path.abspath(__file__))
        history_path = os.path.join(script_directory, "conversation_history.csv")

        with open(history_path, "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(sentence)
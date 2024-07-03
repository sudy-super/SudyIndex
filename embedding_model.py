from sentence_transformers import SentenceTransformer

class CreateEmbedding:
    def __init__(self):
        self.model_multi = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        print("[CHECKPOINT] CreateEmbedding System Startup!")
    def creating_embedding(self, sentences):
        embedding_multi = self.model_multi.encode(sentences)
        print("[CHECKPOINT] Create Embedding!")
        return embedding_multi

if __name__ == "__main__":
    sentence = "起動テスト"
    system = CreateEmbedding()
    response = system.creating_embedding(sentence)
    print(response)
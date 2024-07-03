from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import openai
import settings

class CreateSummary:
    def get_summ_gpt(self, conversation):
        openai.api_key = settings.openai_api_key_set
        messages = []

        initial_content = "提示する会話文を要約してください。"

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
          {"role": "system", "content":f"{initial_content}"},
          {"role": "user", "content": f"{conversation}"}])
        summary_response = response['choices'][0]['message']['content']
        return summary_response

    def __init__sub(self):
        model_checkpoints = "stockmark/bart-base-japanese-news"
        model_directory = ""
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoints, trust_remote_code=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_directory)
        
        print("[CHECKPOINT] Create Summary System Startup!")

    def make_summary_sub(self, conversation, max_input=512, max_target=256):
        model_inputs = self.tokenizer(conversation, max_length=max_input, padding=True, truncation=True, return_tensors='pt')
        raw_pred = self.model.generate(input_ids=model_inputs['input_ids'], attention_mask=model_inputs['attention_mask'], max_length=max_target, do_sample=False)
        response = self.tokenizer.decode(raw_pred[0], skip_special_tokens=True)

        print("[CHECKPOINT] Made Summary!")
        
        return response

if __name__ == "__main__":
    conversation = """
    """
    summary_instance = CreateSummary()
    back = summary_instance.make_summary(conversation)
    print(back)
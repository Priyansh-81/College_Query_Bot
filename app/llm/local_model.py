from app.config import model_name
from app.llm.prompts import system_prompt
import ollama

class LLMModel:
    def __init__(self):
        self.model=model_name

    def generate_response(self, prompt:str)->str:
        question=prompt.strip()
        if not question:
            raise ValueError("Please provide a valid question.")
        try:
            response=ollama.chat(model=self.model,
                                 messages=[{
                                     "role":"system",
                                     "content":system_prompt,   
                                 }, 
                                 {
                                     "role":"user",
                                     "content":question,
                                 }
                                 ]
                                 )
            return response.message.content.strip()
        except ollama.ResponseError as e:
            raise RuntimeError(f"Error generating response: {e}") from e
        
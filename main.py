from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class InstructLLM:
    def __init__(self, model_name="gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate_response(self, instruction, max_length=100):
        # Formatiere den Prompt im Instruction-Format
        prompt = f"Instruction: {instruction}\nResponse:"
        
        # Tokenisiere den Input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Generiere die Antwort
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Dekodiere und gib die Antwort zurück
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("Response:")[-1].strip()

def main():
    # Initialisiere das Modell
    llm = InstructLLM()
    
    # Beispiel-Instruktionen
    instructions = [
        "Erkläre mir das Konzept von künstlicher Intelligenz in einem Satz.",
        "Schreibe ein kurzes Gedicht über Programmierung.",
        "Gib mir drei Tipps zum effektiven Lernen."
    ]
    
    # Generiere und zeige Antworten
    for instruction in instructions:
        print(f"\nInstruction: {instruction}")
        response = llm.generate_response(instruction)
        print(f"Response: {response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()

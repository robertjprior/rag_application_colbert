from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model = 'ericzzz/falcon-rw-1b-instruct-openorca'

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
   'text-generation',
   model=model,
   tokenizer=tokenizer,
   torch_dtype=torch.bfloat16,
   device_map='auto',
)

with open("tmp/out.txt", "r") as f:
    context = f.read()

system_message = 'Using the context to come, answer this question in a succint manner'
instruction = "what is shot scraper? "
prompt = f'<SYS> {system_message} <INST> {instruction} \n Context: {context} END CONTEXT <RESP> '

response = pipeline(
   prompt, 
   max_length=5000,
   #repetition_penalty=1.05,
   trucation=True
)

print(response[0]['generated_text'])

with open("tmp/llm_response.txt", "w") as f:
    f.write(response[0]['generated_text'])
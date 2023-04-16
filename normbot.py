import os
from langchain.llms import OpenAI
from llama_index import GPTSimpleVectorIndex
os.environ['OPENAI_API_KEY'] = "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"

# Load you data into 'Documents' a custom type by LlamaIndex

from llama_index import SimpleDirectoryReader

documents = SimpleDirectoryReader(r"C:\Users\taash\Downloads\FYPAPP\data").load_data()
# Create an index of your documents

from llama_index import GPTSimpleVectorIndex

index = GPTSimpleVectorIndex(documents)
# Query your index!

response = index.query("What do you think of Facebook's LLaMa?")
print(response)

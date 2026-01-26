from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.llms import ChatMessage

llm = Ollama(model="llama3", base_url="http://localhost:11434", request_timeout=300.0)
response = llm.complete("What is the capital of France?")
print(response.text)

messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="What is your name"),
]
resp = llm.chat(messages)
print(resp)

from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="embeddinggemma:300m",
    base_url="http://localhost:11434"
)

result = embeddings.embed_query("hello world")

print(len(result))
print(result[:5])
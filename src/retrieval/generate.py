# src/retrieval/generate.py

import argparse
import os
import sys
from dotenv import load_dotenv

# Add the parent directory of 'retrieval' (which is 'src') to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from ingestion.embed import get_embedding_function

# Load environment variables from .env file
load_dotenv()

CHROMA_PATH = "db/"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    # Initialize the Google Gemini model
    # The API key is automatically picked up from the .env file.
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    
    # Get the response from the model
    response = model.invoke(prompt)

    print("--- RESPONSE ---")
    print(response.content)


if __name__ == "__main__":
    main()

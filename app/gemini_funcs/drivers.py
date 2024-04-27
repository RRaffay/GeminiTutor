from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate


import json
import requests

import google.generativeai as genai
import google.ai.generativelanguage as glm


load_dotenv()

# Access dotenv variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

SERP_API_KEY = os.getenv('SERP_API_KEY')


def google_search_runner(search_keyword: str):
    """Returns the google results for the given search word"""
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": search_keyword
    })

    headers = {
        'X-API-KEY': SERP_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"Google Search for: {search_keyword}")
    return response.text


google_search = {'function_declarations': [
    {
        "name": "google_search",
        "description": "Google search to return results of search keywords",
        "parameters": {
            "type_": "OBJECT",
            "properties": {
                "search_keyword": {
                    "type_": "STRING",
                    "description": "A great search keyword that most likely to return resuls for the information you are looking for"
                }
            },
            "required": [
                "search_keyword"
            ]
        }
    }
]}


def article_reader_runner(url: str):
    "Given a url, this returns the summary of the article"
    print(f"Reading article: {url}")
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", google_api_key=GOOGLE_API_KEY)

    # Load the blog
    loader = WebBaseLoader(url)
    docs = loader.load()

    # Define the Summarize Chain
    template = """Write a concise summary of the following:
  "{text}"
  CONCISE SUMMARY:"""

    prompt = PromptTemplate.from_template(template)

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(
        llm_chain=llm_chain, document_variable_name="text")

    # Invoke Chain
    response = stuff_chain.invoke(docs)
    return response["output_text"]


article_summarizer = {'function_declarations': [
    {
        "name": "article_summarizer",
        "description": "Reads article given a url: Returns summary of article",
        "parameters": {
            "type_": "OBJECT",
            "properties": {
                "url": {
                      "type_": "STRING",
                      "description": "URL of the webpage to be read"
                      }
            },
            "required": [
                "url"
            ]
        }
    }
]}


def handle_response(response, chat):
    if response.candidates[0].content.parts[0].function_call.name == "google_search":
        fc = response.candidates[0].content.parts[0].function_call
        key_word = fc.args["search_keyword"]
        result = google_search_runner(key_word)
        response = chat.send_message(
            glm.Content(
                parts=[glm.Part(
                    function_response=glm.FunctionResponse(
                        name='google_search',
                        response={'result': result}))]))
        return response
    elif response.candidates[0].content.parts[0].function_call.name == "article_summarizer":
        fc = response.candidates[0].content.parts[0].function_call
        url_arg = fc.args['url']
        result = article_reader_runner(url_arg)
        response = chat.send_message(
            glm.Content(
                parts=[glm.Part(
                    function_response=glm.FunctionResponse(
                        name='article_summarizer',
                        response={'result': result}))]))
        return response

    return response


def class_details(class_name, school_name):
    model = genai.GenerativeModel(
        'gemini-pro', tools=[article_summarizer, google_search])
    chat = model.start_chat()
    response = chat.send_message(
        f"Find more information about the {school_name} {class_name} by first searching for articles and then reading from the url. We require a thorough understanding of the course contents and objectives",
    )

    fc = response.candidates[0].content.parts[0].function_call

    while fc:
        response = handle_response(response, chat)
        fc = response.candidates[0].content.parts[0].function_call

    return response.text


def main():
    print(class_details("CS330", "Duke University"))


if __name__ == "__main__":
    main()

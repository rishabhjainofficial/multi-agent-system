from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from rich import print
import requests
import os
from bs4 import BeautifulSoup
from tavily import TavilyClient

@tool
def get_search(query:str) -> str:
    """
    Returns Tites, URLs and Snippets from the search results for the given query.
    """
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = tavily.search(query=query, max_results=5)

    out = []

    for r in results["results"]:
        out.append(f"Title: {r['title']} \n URL: {r['url']} \n Snippet: {r['content'][:300]}")

    return "\n--------\n".join(out)

@tool
def scrape_url(url:str) ->str:
    """
    Scrapes the content from the given URL.
    """
    try:
        response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(['script','style','nav','footer']):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

if __name__ == "__main__":
    print(scrape_url.invoke({"url": "https://cloud.google.com/learn/what-is-artificial-intelligence"}))

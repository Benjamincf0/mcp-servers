import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from serpapi import GoogleSearch
import json

mcp = FastMCP()

if not load_dotenv():
    raise FileNotFoundError("No .env file found")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in .env file")


@mcp.tool()
def job_search(query: str, num_results: int = 1) -> str:
    """Searches for jobs on Google

    Args:
        query (str): The search query
        num_results (int, optional): The number of results to return. Defaults to 1.

    Returns:
        str: The results of the search
    """
    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "api_key": API_KEY,
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        jobs = results["jobs_results"]
    except Exception:
        return "Search failed"

    return json.dumps(jobs[:num_results], ensure_ascii=False)


def main():
    # run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

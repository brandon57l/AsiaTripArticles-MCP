
import requests
import json

# The base URL for the deployed Travel Articles API.
BASE_URL = "https://asiantriparticles-api.onrender.com/api"

def search_articles(keywords: list):
    """
    Searches for articles by a list of keywords.
    Corresponds to GET /api/articles/search?q=keyword1,keyword2
    """
    if not keywords:
        return {"error": "Keyword list cannot be empty."}
    
    query_string = ",".join(keywords)
    url = f"{BASE_URL}/articles/search"
    params = {'q': query_string}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

def get_article_by_id(article_id: str):
    """
    Retrieves a full article by its unique ID.
    Corresponds to GET /api/articles/<article_id>
    """
    url = f"{BASE_URL}/articles/{article_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

def get_article_table_of_contents(article_id: str):
    """
    Gets the table of contents for a specific article.
    Corresponds to GET /api/articles/<article_id>/toc
    """
    url = f"{BASE_URL}/articles/{article_id}/toc"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

def get_article_section_by_title(article_id: str, section_title: str):
    """
    Retrieves a specific section from an article by its title.
    Corresponds to GET /api/articles/<article_id>/sections/<section_title>
    """
    # The requests library automatically handles URL encoding for path segments.
    url = f"{BASE_URL}/articles/{article_id}/sections/{section_title}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

if __name__ == '__main__':
    # Example usage - you can run this file directly to test the client
    print("--- Testing Article Search ---")
    search_results = search_articles(["tokyo", "food"])
    print(json.dumps(search_results, indent=2))

    if search_results and 'data' in search_results and search_results['data']:
        # Get the ID of the first article from the search results
        first_article_id = search_results['data'][0]['_id']
        
        print(f"\n--- Testing Get Article by ID ({first_article_id}) ---")
        article_details = get_article_by_id(first_article_id)
        print(json.dumps(article_details, indent=2))

        print(f"\n--- Testing Get TOC for Article ({first_article_id}) ---")
        toc = get_article_table_of_contents(first_article_id)
        print(json.dumps(toc, indent=2))

        if toc and 'data' in toc and toc['data']['table_of_contents']:
            first_section = toc['data']['table_of_contents'][0]
            print(f"\n--- Testing Get Section '{first_section}' for Article ({first_article_id}) ---")
            section_details = get_article_section_by_title(first_article_id, first_section)
            print(json.dumps(section_details, indent=2))


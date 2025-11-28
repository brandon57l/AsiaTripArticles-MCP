import api_client

# This file defines a list of "tools" that the MCP can use.
# Each tool is a wrapper around a function from the api_client.
# This structure makes it easy for an agent to understand the available capabilities.

def search_article_by_keyword_tool(keyword: str):
    """
    Tool to search for articles by a single keyword.
    """
    return api_client.search_articles_by_keyword(keyword)

def get_article_by_id_tool(article_id: str):
    """
    Tool to retrieve a full article by its ID.
    """
    return api_client.get_article_by_id(article_id)

def get_article_toc_tool(article_id: str):
    """
    Tool to get the table of contents for an article by its ID.
    """
    return api_client.get_article_table_of_contents(article_id)

def get_article_section_tool(article_id: str, section_title: str):
    """
    Tool to retrieve a specific section of an article.
    """
    return api_client.get_article_section_by_title(article_id, section_title)

# A list that describes all the available tools.
# An agent could use this list to decide which function to call.
available_tools = [
    {
        "name": "search_article_by_keyword",
        "description": "(Step 1) Searches for travel articles based on a single keyword. Use this first to find relevant articles and obtain their IDs. If the initial search yields no results, try using different, similar keywords. Always evaluate the returned content to determine its relevance. After this, consider using 'get_article_table_of_contents' with an article ID.",
        "function": search_article_by_keyword_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "A single keyword (e.g., 'tokyo')."
                }
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "get_article_table_of_contents",
        "description": "(Step 2) Retrieves the table of contents (a list of section titles) for a specific article using its unique ID. Use this after 'search_article_by_keyword' to understand the article's structure. After this, consider using 'get_article_section' with an article ID and a section title.",
        "function": get_article_toc_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "article_id": {
                    "type": "string",
                    "description": "The unique identifier of the article."
                }
            },
            "required": ["article_id"]
        }
    },
    {
        "name": "get_article_section",
        "description": "(Step 3) Retrieves the content of a specific section from an article using its unique ID and the section's title. Use this after 'get_article_table_of_contents' to get targeted content. If the required information is not found in a specific section, consider using 'get_article_details' to retrieve the full article.",
        "function": get_article_section_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "article_id": {
                    "type": "string",
                    "description": "The unique identifier of the article."
                },
                "section_title": {
                    "type": "string",
                    "description": "The exact title of the section to retrieve."
                }
            },
            "required": ["article_id", "section_title"]
        }
    },
    {
        "name": "get_article_details",
        "description": "(Step 4 - Optional) Gets the full content and details of a specific article using its unique ID. Use this as a last resort if 'get_article_section' does not provide sufficient information, or if you need the entire article content.",
        "function": get_article_by_id_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "article_id": {
                    "type": "string",
                    "description": "The unique identifier of the article."
                }
            },
            "required": ["article_id"]
        }
    }
]

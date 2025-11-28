import api_client

# This file defines a list of "tools" that the MCP can use.
# Each tool is a wrapper around a function from the api_client.
# This structure makes it easy for an agent to understand the available capabilities.

def search_articles_tool(keywords_str: str):
    """
    Tool to search for articles.
    Expects a single string of comma-separated keywords.
    Example: "japan,sushi"
    """
    keywords = [keyword.strip() for keyword in keywords_str.split(',')]
    return api_client.search_articles(keywords)

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
        "name": "search_articles",
        "description": "Searches for travel articles based on a comma-separated list of keywords.",
        "function": search_articles_tool,
        "parameters": {
            "type": "object",
            "properties": {
                "keywords_str": {
                    "type": "string",
                    "description": "A string of comma-separated keywords (e.g., 'tokyo,food')."
                }
            },
            "required": ["keywords_str"]
        }
    },
    {
        "name": "get_article_details",
        "description": "Gets the full content and details of a specific article using its unique ID.",
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
    },
    {
        "name": "get_article_table_of_contents",
        "description": "Retrieves the table of contents (a list of section titles) for a specific article.",
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
        "description": "Retrieves the content of a specific section from an article.",
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
    }
]

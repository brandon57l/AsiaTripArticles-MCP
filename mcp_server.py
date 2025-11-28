import json
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os

# On importe les outils que nous avons créés.
# Ces outils savent comment parler à votre API sur Render.
from tools import (
    search_articles_tool,
    get_article_by_id_tool,
    get_article_toc_tool,
    get_article_section_tool
)

# 1. Création du serveur MCP
mcp = FastMCP("TravelArticleAssistant", debug=True)

# 2. Enregistrement des outils existants auprès de MCP
# La décoration @mcp.tool() est la manière moderne de le faire.
# On enveloppe simplement les fonctions existantes.

@mcp.tool()
def search_articles(query: str) -> str:
    """
    Cherche des articles contenant des mots-clés spécifiques.
    Par exemple: 'tokyo,food'
    """
    return json.dumps(search_articles_tool(query))

@mcp.tool()
def get_article_by_id(article_id: str) -> str:
    """
    Récupère le contenu complet d'un article en utilisant son identifiant unique (ID).
    """
    return json.dumps(get_article_by_id_tool(article_id))

@mcp.tool()
def get_article_toc(article_id: str) -> str:
    """
    Récupère la table des matières (la liste des sections) pour un article donné.
    """
    return json.dumps(get_article_toc_tool(article_id))

@mcp.tool()
def get_article_section(article_id: str, section_title: str) -> str:
    """
    Récupère le contenu d'une section spécifique d'un article.
    """
    return json.dumps(get_article_section_tool(article_id, section_title))

# --- POINT D'ENTRÉE PRINCIPAL (Inspiré de votre exemple) ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Initialisation du serveur MCP sur le port {port}...")

    # 1. Récupération de l'application Starlette interne depuis FastMCP
    try:
        app_core = mcp.sse_app()
    except TypeError:
        app_core = mcp.sse_app

    # 2. Middleware CORS (Indispensable pour les clients web)
    app = CORSMiddleware(
        app_core,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 3. Lancement avec Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

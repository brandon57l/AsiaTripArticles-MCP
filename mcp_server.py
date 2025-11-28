import json
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os

# On importe les outils que nous avons créés.
# Ces outils savent comment parler à votre API sur Render.
from tools import (
    search_article_by_keyword_tool,
    get_article_by_id_tool,
    get_article_toc_tool,
    get_article_section_tool
)

# 1. Création du serveur MCP
mcp = FastMCP("TravelArticleAssistant", debug=True)

# 2. Enregistrement des outils existants auprès de MCP
# La décoration @mcp.tool() est la manière moderne de le faire.
# On enveloppe simplement les fonctions existantes.

# ÉTAPE 1: Le point de départ. Cherchez des articles avec un mot-clé.
# Après cette étape, vous obtiendrez des identifiants d'articles (ID) que vous pourrez utiliser pour les étapes suivantes.
@mcp.tool()
def search_article_by_keyword(query: str) -> str:
    """
    Searches for articles containing a specific keyword.
    For example: 'tokyo'
    """
    return json.dumps(search_article_by_keyword_tool(query))

# ÉTAPE 2: Une fois que vous avez un ID d'article, obtenez sa structure.
# Après avoir cherché des articles, utilisez cette fonction avec un ID obtenu pour voir la table des matières.
@mcp.tool()
def get_article_toc(article_id: str) -> str:
    """
    Récupère la table des matières (la liste des sections) pour un article donné.
    C'est utile pour avoir un aperçu du contenu avant de tout charger.
    """
    return json.dumps(get_article_toc_tool(article_id))

# ÉTAPE 3: Plongez dans une section spécifique qui vous intéresse.
# Après avoir obtenu la table des matières, utilisez cette fonction avec un ID d'article et un titre de section pour récupérer une section spécifique.
@mcp.tool()
def get_article_section(article_id: str, section_title: str) -> str:
    """
    Récupère le contenu d'une section spécifique d'un article.
    C'est plus efficace que de récupérer l'article entier si seule une partie vous intéresse.
    """
    return json.dumps(get_article_section_tool(article_id, section_title))

# ÉTAPE 4 (Optionnel): Si vous avez besoin de tout, récupérez l'article complet.
# Si, après avoir consulté les sections, vous souhaitez l'article entier, utilisez cette fonction avec l'ID de l'article.
@mcp.tool()
def get_article_by_id(article_id: str) -> str:
    """
    Récupère le contenu complet d'un article en utilisant son identifiant unique (ID).
    À utiliser lorsque la recherche par section n'est pas suffisante.
    """
    return json.dumps(get_article_by_id_tool(article_id))

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

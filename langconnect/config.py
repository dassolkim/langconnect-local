import json

from langchain_core.embeddings import Embeddings
from starlette.config import Config, undefined

env = Config()

IS_TESTING = env("IS_TESTING", cast=str, default="").lower() == "true"

if IS_TESTING:
    SUPABASE_URL = ""
    SUPABASE_KEY = ""
else:
    SUPABASE_URL = env("SUPABASE_URL", cast=str, default=undefined)
    SUPABASE_KEY = env("SUPABASE_KEY", cast=str, default=undefined)


def get_embeddings() -> Embeddings:
    """Get the embeddings instance based on the environment."""
    # Check if we should use Ollama instead of OpenAI
    use_ollama = env("USE_OLLAMA_EMBEDDINGS", cast=str, default="false").lower() == "true"
    
    if use_ollama:
        from langchain_ollama import OllamaEmbeddings
        ollama_model = env("OLLAMA_EMBEDDING_MODEL", cast=str, default="nomic-embed-text")
        ollama_base_url = env("OLLAMA_BASE_URL", cast=str, default="http://localhost:11435")
        
        return OllamaEmbeddings(
            model=ollama_model,
            base_url=ollama_base_url
        )
    else:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model="text-embedding-3-small")


DEFAULT_EMBEDDINGS = get_embeddings()
DEFAULT_COLLECTION_NAME = "default_collection"


# Database configuration
POSTGRES_HOST = env("POSTGRES_HOST", cast=str, default="localhost")
POSTGRES_PORT = env("POSTGRES_PORT", cast=int, default="5432")
POSTGRES_USER = env("POSTGRES_USER", cast=str, default="langchain")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD", cast=str, default="langchain")
POSTGRES_DB = env("POSTGRES_DB", cast=str, default="langchain_test")

# Read allowed origins from environment variable
ALLOW_ORIGINS_JSON = env("ALLOW_ORIGINS", cast=str, default="")

if ALLOW_ORIGINS_JSON:
    ALLOWED_ORIGINS = json.loads(ALLOW_ORIGINS_JSON.strip())
    print(f"ALLOW_ORIGINS environment variable set to: {ALLOW_ORIGINS_JSON}")
else:
    ALLOWED_ORIGINS = "http://localhost:3000"
    print("ALLOW_ORIGINS environment variable not set.")

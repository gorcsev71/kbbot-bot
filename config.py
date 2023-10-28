
import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = os.environ.get("PORT") # 3978 / 8000
    HOST = os.environ.get("HOST") # localhost / 0.0.0.0
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_EMBEDDING_MODEL = os.environ.get('OPENAI_EMBEDDING_MODEL')
    OPENAI_MODEL_NAME = os.environ.get('OPENAI_MODEL_NAME')
    AZURE_COGNITIVE_SEARCH_SERVICE_NAME = os.environ.get('AZURE_COGNITIVE_SEARCH_SERVICE_NAME')
    AZURE_COGNITIVE_SEARCH_API_KEY = os.environ.get('AZURE_COGNITIVE_SEARCH_API_KEY')
    AZURE_COGNITIVE_SEARCH_INDEX_NAME = os.environ.get('AZURE_COGNITIVE_SEARCH_INDEX_NAME')
    

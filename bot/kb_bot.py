from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

from config import DefaultConfig

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import Vector
import openai


def search_for_answer(query:str)->str:
    print(query)
    APP_CONFIG = DefaultConfig()
    search_client = SearchClient(f"https://{APP_CONFIG.AZURE_COGNITIVE_SEARCH_SERVICE_NAME}.search.windows.net"
                                 ,APP_CONFIG.AZURE_COGNITIVE_SEARCH_INDEX_NAME,
                                 AzureKeyCredential(APP_CONFIG.AZURE_COGNITIVE_SEARCH_API_KEY))
    openai.api_key = APP_CONFIG.OPENAI_API_KEY
    embedding = openai.Embedding.create(input=query,
                                        deployment_id=APP_CONFIG.OPENAI_EMBEDDING_MODEL)["data"][0]["embedding"]
    vector = Vector(value=embedding, k=3, fields="content_vector")
    results = search_client.search(
        search_text="",
        vectors=[vector],
        select=["document_name", "content_text"]
    )
    answer = ""
    print("Results:")
    for result in results:
        score = result["@search.score"]
        print(f"- {result['document_name']}, {result['@search.score']}")
        answer += result["content_text"] + " "

    system_prompt = "Answer the question based on the below knowledge base. If the answer cannot be found in the knowledge base, reply 'I could not find the answer in my knowledge base.'. Here is your knowledge base: " + answer
    chat_messages = [{"role": "system", "content": system_prompt}]
    message = query
    chat_messages.append({"role": "user", "content": message},)
    chat = openai.ChatCompletion.create(model=APP_CONFIG.OPENAI_MODEL_NAME,
                                        messages=chat_messages)
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    # TODO: Add the sources as well
    return reply

class KBBot(ActivityHandler):
    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_text = "Hey, I am your HR Bot. Ask me about the onboarding and offboarding process. "
                await turn_context.send_activity(welcome_text)

    async def on_message_activity(self, turn_context: TurnContext):
        query = turn_context.activity.text
        answer = search_for_answer(query)
        return await turn_context.send_activity(
            MessageFactory.text(answer)
        )
    
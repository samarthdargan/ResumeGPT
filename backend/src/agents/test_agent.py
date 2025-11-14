from agent_framework.azure import AzureOpenAIChatClient
from ..config import settings

class TestAgent:
    def __init__(self):
        self.client = AzureOpenAIChatClient(
            endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME
        )

    async def test_connection(self) -> bool:
        try:
            response = await self.client.chat.complete(
                messages=[{"role": "system", "content": "Hello, world!"}]
            )
            return response is not None
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
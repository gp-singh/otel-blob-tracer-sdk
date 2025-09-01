from openai import AsyncAzureOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
import chainlit as cl
import os


AZURE_OPENAI_ENDPOINT = "https://az-oai-gp.openai.azure.com/"
AZURE_OPENAI_API_KEY = "6hyV7Ue8Dw3V4w2Ier9qCc4Y6ITivK2kDK2YKmONiY8hwYWX5sgJQQJ99ALAC4f1cMXJ3w3AAABACOGoVMP"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
AZURE_OPENAI_DEPLOYMENT = "o4-mini"
AZURE_OPENAI_DEPLOYMENT_ENDPOINT = "https://az-oai-gp.openai.azure.com/openai/deployments/o4-mini/chat/completions?api-version=2025-01-01-preview"
AZURE_INFERENCE_ENDPOINT = "https://az-oai-gp.services.ai.azure.com/openai/v1"


# Disable tracing since we're using Azure OpenAI
set_tracing_disabled(disabled=True)



 # Create the Async Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_DEPLOYMENT_ENDPOINT
)

# Configure the agent with Azure OpenAI
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(
        model=AZURE_OPENAI_DEPLOYMENT,
        openai_client=client,
    )
)

"""The main function will be called every time a user inputs a message in the chatbot UI.
 You can put your custom logic within the function to process the users input, 
 such as analyzing the text, calling an API, or computing a result."""

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
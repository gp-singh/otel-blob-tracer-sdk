import os
import asyncio
from openai import AsyncAzureOpenAI
from openai import OpenAIError
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled

import chainlit as cl

# Disable tracing since we're using Azure OpenAI
set_tracing_disabled(disabled=True)

deployment = "gpt-4o"


async def main():
    try:
        # Create the Async Azure OpenAI client
        client = AsyncAzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2023-09-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

        # Configure the agent with Azure OpenAI
        agent = Agent(
            name="Assistant",
            instructions="You are a helpful assistant",
            model=OpenAIChatCompletionsModel(
                model=deployment,
                openai_client=client,
            )
        )

        handle_message(agent, cl.Message(content="Write a haiku about recursion in programming."))
        #result = await Runner.run(agent, "Write a haiku about recursion in programming.")
        #print(result.final_output)

    except OpenAIError as e:
        print(f"OpenAI API Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

@cl.on_message
async def handle_message(agent: Agent, message: cl.Message):
    query = message.content
    cl.user_session.set("query", query)

    result = Runner.run(agent, "Write a haiku about recursion in programming.")
    await cl.Message(content=f" Here's the respone: \n {result}").send()

if __name__ == "__main__":
    asyncio.run(main())
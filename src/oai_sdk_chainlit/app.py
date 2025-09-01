# app.py
import chainlit as cl
from agents import multi_agent

@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content
    cl.user_session.set("query", query)

    # Step 1: Web search
    result = multi_agent.run(f"search_web: {query}")
    await cl.Message(content=f"🔎 Explorer Agent found:\n{result}").send()

    # Step 2: Summarization
    summary = multi_agent.run(f"summarize_text: {result}")
    await cl.Message(content=f"📚 Synthesizer Agent summary:\n{summary}").send()

    # Step 3: Planning
    plan = multi_agent.run(f"plan_actions: {summary}")
    await cl.Message(content=f"🧭 Planner Agent suggests:\n{plan}").send()
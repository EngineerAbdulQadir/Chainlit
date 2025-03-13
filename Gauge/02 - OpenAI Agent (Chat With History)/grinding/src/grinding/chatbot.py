import os
import chainlit as cl

from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Step 1 - Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Step 2 - Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Step 3 - Config
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Step 4 - Agent
agent = Agent(
    instructions="You are a helpful assistant that can answer questions.",
    name="Xactrix AI Support Agent"
)

# Step 5 - Run
# result = Runner.run_sync(
#     agent,
#     input="What is the capital of France?",
#     run_config=config,    
# )

# print(result.final_output)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! I am Xactrix AI Support Agent.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    
    # Standard Interface 
    history.append({"role": "user", "content": message.content})
    
    result = await Runner.run(
        agent,
        input=history,
        run_config=config,
    )
    
    history.append({"role": "assistant", "content": result.final_output})
    
    cl.user_session.set("history", history)
    
    await cl.Message(
        content=result.final_output,
    ).send()
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter

from groq import Groq
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv, find_dotenv
from tools import weather_tool, forecast_tool
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv(find_dotenv())

api_key = os.getenv("OPENROUTE_API_KEY")

tools = [weather_tool, forecast_tool]

llm = ChatOpenRouter(
    base_url="https://openrouter.ai/api/v1",
    model="nvidia/nemotron-3-nano-30b-a3b:free",  # Free tier model
    tools=tools,
    temperature=0.5,
    api_key=api_key

)


chat_history = []

print("===I am a Weather Ai what can i help you with===\n")
while True:

    user_input = input("You: ")

    if "exit" in user_input.lower() or "quit" in user_input.lower():
        print("\nGoodbye! ")

        chat_history.append(HumanMessage(content=user_input))

        break

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant that ALWAYS uses the available \n"
        "weather tool to get current weather information. Never say you don't have access to weather data."

    )

    chat_history.append(HumanMessage(content=user_input))

    research_response = agent.invoke({
        "messages": chat_history
    })

    ai_message = research_response["messages"][-1].content
    chat_history.append(AIMessage(content=ai_message))

    print(f"\nAI: {ai_message}")

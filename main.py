import os
from langchain_groq import ChatGroq
from groq import Groq
from langchain.agents import create_agent
from dotenv import load_dotenv, find_dotenv
from tools import weather_tool


load_dotenv(find_dotenv())

api_key = os.getenv("GROQ_API_KEY")

tools = [weather_tool]

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    tools=tools,
    temperature=0.5,
    api_key=api_key

)

user_input = input("I am a Weather Ai what can i help you with\n")

if "weather" in user_input.lower():
    city = user_input.split("in")[-1].strip()

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant that ALWAYS uses the available \n"
        "weather tool to get current weather information. Never say you don't have access to weather data."

    )

    research_response = agent.invoke({
        "messages": [("user", user_input)]
    })

    print(f"\n{research_response["messages"][-1].content}")

else:
    print("I only answer weather realated prompts")

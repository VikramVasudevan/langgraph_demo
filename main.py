from typing import TypedDict, override
from langgraph.constants import END, START
from langgraph.graph.state import StateGraph
from typing_extensions import Annotated
from pydantic import BaseModel
from langgraph.graph.message import add_messages
import gradio as gr
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o-mini")


def chatNode(state: State):
    messages = state["messages"]
    print("messages = ",messages)
    responseMessage =  llm.invoke(messages)
    newState = State(messages=[responseMessage])
    return newState


def encryptNode(state: State):
    messages = state["messages"]
    messages[-1].content += "ASDFGHJKL"
    newState = State(messages=messages)
    return newState


graph_builder.add_node("MyChatNode", chatNode)
graph_builder.add_node("MyEncryptNode", encryptNode)
graph_builder.add_edge(START, "MyChatNode")
graph_builder.add_edge("MyChatNode", "MyEncryptNode")
graph_builder.add_edge("MyEncryptNode", END)
graph = graph_builder.compile()


def chat(message, history):
    # Ensure history is a list of message dicts
    if not history:
        history = []
    initial_state = State(messages=history + [{"role" : "user" , "content" : message}])
    print("initial_state = ", initial_state)
    response = graph.invoke(initial_state)
    return response["messages"][-1].content


def main():
    print("Hello from langgraph-demo!")
    gr.ChatInterface(chat, type="messages").launch()


if __name__ == "__main__":
    main()

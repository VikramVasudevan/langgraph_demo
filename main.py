from typing import TypedDict
from langgraph.constants import END, START
from langgraph.graph.state import StateGraph
from typing_extensions import Annotated
from pydantic import BaseModel
from langgraph.graph.message import add_messages
import gradio as gr


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatNode(state: State):
    messages = state["messages"]
    print("messages = ",messages)
    message_count = len(messages)
    print("message_count = ", message_count)
    responseMessage = {
        "role": "assistant",
        "content": f"this was message #{message_count}.",
    }
    newState = State(messages=[responseMessage])
    return newState


graph_builder.add_node("MyChatNode", chatNode)
graph_builder.add_edge(START, "MyChatNode")
graph_builder.add_edge("MyChatNode", END)
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

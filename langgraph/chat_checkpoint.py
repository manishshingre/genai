from typing_extensions import TypedDict
from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph.message import  add_messages
from langgraph.graph import StateGraph, START, END
from os import getenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.mongodb import MongoDBSaver


load_dotenv()
gemini_api_key = getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2
)
class State(TypedDict):
    messages: Annotated[list, add_messages]
    
def chatbot(state: State) -> State:
    response = model.invoke(state.get("messages"))
    return { "messages": [response] }
    
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    config= {
        "configurable": {
            "thread_id": "manish"
        }
    }

    for chunk in graph_with_checkpointer.stream(
        State({"messages": ["Hello, WHAT am I learning"]}),
        config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()
from typing_extensions import TypedDict
from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph.message import  add_messages
from langgraph.graph import StateGraph, START, END
from os import getenv
from langchain_google_genai import ChatGoogleGenerativeAI

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

def samplenode(state: State) -> State:
    print("Inside sample node", state)
    return { "messages": ["\nMessage from the sample node."] }
    
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_graph = graph.invoke(State({"messages": ["Hello my name is Shahrukh Khan."]}))
print("Updated graph:", updated_graph)
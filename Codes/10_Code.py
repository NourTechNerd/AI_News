import dotenv
import os
from langgraph.store.memory import InMemoryStore

import uuid
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.base import BaseStore
from langchain_google_genai import ChatGoogleGenerativeAI

dotenv.load_dotenv()

## We Initialize the Memory here
in_memory_store = InMemoryStore()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key = os.getenv("GOOGLE_API_KEY"))

# Define The LLM Node Function

def LLM_node_function(state: MessagesState, config: RunnableConfig, store: BaseStore):
    user_id = config["configurable"]["user_id"]
    user_namespace = ("memories", user_id)
    # Fetch the User namespace where there are all memories about the user
    
    memories = store.search(user_namespace)
    print("Memories",memories)
    info = "\n".join([d.value["data"] for d in memories])
    print("Info",info)
    system_msg = f"You are a helpful assistant talking to the user. User info: {info}"

    # Store new memories if the user asks the model to remember
    last_message = state["messages"][-1]
    if "remember" in last_message.content.lower():
        memory = last_message.content
        memory_id = str(uuid.uuid4())
        store.put(user_namespace, memory_id, {"data": memory})
        

    response = llm.invoke(
        [{"type": "system", "content": system_msg}] + state["messages"]
    )
    return {"messages": response}


builder = StateGraph(MessagesState)
builder.add_node("Bot", LLM_node_function)
builder.add_edge(START, "Bot")

# NOTE: we're passing the store object here when compiling the graph
graph = builder.compile(checkpointer=MemorySaver(), store=in_memory_store)

# Run the Graph
config = {"configurable": {"thread_id": "1", "user_id": "1"}}
input_message = {"type": "user", "content": "Hi! Remember: my name is Bob"}
for chunk in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
    chunk["messages"][-1].pretty_print()


## Check the memories are Stored or Not

for memory in in_memory_store.search(("memories", "1")):
     print(memory.value)


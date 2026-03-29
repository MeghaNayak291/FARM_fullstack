from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import uvicorn
from dal import ToDoDAL, ListSummary, ToDoList
from dotenv import load_dotenv  # only needed for local testing

client = AsyncIOMotorClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000,
    tls=True,
    tlsAllowInvalidCertificates=True
)

import os
from motor.motor_asyncio import AsyncIOMotorClient

# Read MongoDB URI from environment (Render will provide it)
MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not set!")

# Connect to MongoDB
client = AsyncIOMotorClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000,
    tls=True,
    tlsAllowInvalidCertificates=True
)
db = client.get_database()
print("MongoDB connected successfully!")
# ------------------------
# Load environment variables (local only)
load_dotenv()  # safe for Render, will just do nothing if no .env

# ------------------------
# Read MongoDB URI from environment
MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable not set!")

# Debug mode (optional)
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}

# Collection name
COLLECTION_NAME = "todo_lists"

print("MongoDB URI loaded:", MONGODB_URI)
print("Debug mode:", DEBUG)

# ------------------------
# Lifespan for FastAPI to manage DB connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    try:
        database = client.get_default_database()
        pong = await database.command("ping")
        if int(pong["ok"]) != 1:
            raise Exception("MongoDB cluster ping failed!")
        app.todo_dal = ToDoDAL(database.get_collection(COLLECTION_NAME))
        print("MongoDB connected successfully!")
        yield
    finally:
        client.close()

# ------------------------
# FastAPI app
app = FastAPI(lifespan=lifespan, debug=DEBUG)

# CORS (adjust front-end URL as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # update if deployed frontend elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Pydantic models
class NewList(BaseModel):
    name: str

class NewItem(BaseModel):
    label: str

class ListItemCheckedState(BaseModel):
    item_id: str
    checked_state: bool

# ------------------------
# Routes
@app.get("/api/lists")
async def get_all_lists() -> list[ListSummary]:
    return [i async for i in app.todo_dal.list_todo_lists()]

@app.post("/api/lists", status_code=status.HTTP_201_CREATED)
async def create_todo_list(new_list: NewList) -> str:
    return await app.todo_dal.create_todo_list(new_list.name)

@app.get("/api/lists/{list_id}")
async def get_list(list_id: str) -> ToDoList:
    return await app.todo_dal.get_todo_list(list_id)

@app.delete("/api/lists/{list_id}")
async def delete_list(list_id: str) -> bool:
    return await app.todo_dal.delete_todo_list(list_id)

@app.post("/api/lists/{list_id}/items", status_code=status.HTTP_201_CREATED)
async def create_item(list_id: str, new_item: NewItem) -> ToDoList:
    return await app.todo_dal.create_item(list_id, new_item.label)

@app.patch("/api/lists/{list_id}/checked_state")
async def set_checked_state(list_id: str, update: ListItemCheckedState) -> ToDoList:
    return await app.todo_dal.set_checked_state(list_id, update.item_id, update.checked_state)

@app.delete("/api/lists/{list_id}/items/{item_id}")
async def delete_item(list_id: str, item_id: str) -> ToDoList:
    return await app.todo_dal.delete_item(list_id, item_id)

# ------------------------
# Run locally
if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
from fastapi import FastAPI, Body
from pymongo import MongoClient
from bson import ObjectId

from pydantic import BaseModel

class Item(BaseModel):
    sensibleId: int
    name: str
    price: int

MONGO_URL = "mongodb connection string"

client = MongoClient(MONGO_URL)
db = client["FastAPI"]
collection = db["items"]

if MongoClient is not None:
    print("Connected to MongoDB successfully!")


app = FastAPI()


@app.post("/items")
def create_item(item: Item):
    result = collection.insert_one(item.dict())
    return {"inserted_id": str(result.inserted_id)}


@app.get("/items/{price}")
def read_item(price: float):
    print(f"Fetching item with price: {price}")
    item = collection.find_one({"price": price})
    if item:
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
        return item
    else:
        return {"error": "Item not found"}
    
    
@app.put("/items/change/{name}")
def update_item(name: str, data: dict):
    collection.update_one({"name": name}, {"$set": data})
    return {"message": "Item updated successfully"}


@app.delete("/items/delete/{price}")
def delete_item(price: float):
    collection.delete_one({"price": price})
    return {"message": "Item deleted successfully"}

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

#Health check endpoint  
@app.get("/health")
def health():
    return {"status": "active"}



cart = []

class Item(BaseModel):
    item: str

@app.post("/cart/add")
def add_to_cart(request: Item):
    cart.append(request.item)
    return {"message": f"{request.item} added to cart", "cart": cart}

@app.get("/cart")
def view_cart():    return {"cart": cart}  

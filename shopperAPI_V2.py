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
def add_to_cart(item : str):
    cart.append(item)
    return {"message": f"{item} added to cart", "cart": cart}

@app.get("/cart")
def view_cart():    return {"cart": cart} 


#Now we will remove items from the cart using a DELETE endpoint

@app.delete("/cart/remove")
def remove_from_cart(item: str):
    if item in cart:
        cart.remove(item)
        return {"message": f"{item} removed from cart", "cart": cart}
    else:
        return {"message": f"{item} not found in cart", "cart": cart}
    
#We can also replace certain items in the cart using a PUT endpoint
@app.put("/cart/replace")
def replace_in_cart(old_item: str, new_item: str):
    if old_item in cart:
        index = cart.index(old_item)
        cart[index] = new_item
        return {"message": f"{old_item} replaced with {new_item} in cart", "cart": cart}
    else:
        return {"message": f"{old_item} not found in cart", "cart": cart}
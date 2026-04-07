from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

#Health check endpoint  
@app.get("/health")
def health():
    return {"status": "active"}



cart = []

@app.post("/cart/add")
def add_to_cart(item: str):
    cart.append(item)
    return {"message": f"{item} added to cart", "cart": cart}

#curl command : curl -X POST http://localhost:8000/cart/add -H "Content-Type: application/json" -d '{"item": "Apple"}'
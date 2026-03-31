import fastapi as fi

app = fi.FastAPI()

@app.get("/")
def root():
    return {
        "over" : "powered"
    }

cart = []

@app.get("/add-to-cart")
def addCart(item: str):
    cart.append(item)
    return {
        "cart" : cart
    }
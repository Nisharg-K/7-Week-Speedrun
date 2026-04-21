from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address 
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler


app = FastAPI()

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "Hello, World!"}







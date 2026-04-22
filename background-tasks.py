from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def send_email(email: str):
    with open("log.txt", "a") as log_file:
        log_file.write(f"Email sent to: {email}\n")


@app.post("/register")
async def register_user(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, "gmail@user.com")

    return {"message": f"User registered with email: {email}"}


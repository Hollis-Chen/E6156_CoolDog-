from fastapi import FastAPI, Response

# I like to launch directly and not use the standard FastAPI startup
import uvicorn


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from groups"}

@app.get("/groups/{name}")
async def Group_name(name: str):
    return {"message": f"Group name is: {name}"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)


import uvicorn

if __name__ == "__main__":
    uvicorn.run("Server.app:app", host="0.0.0.0",  port=8000,lifespan="on", reload=True)

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from routers import notes
import uvicorn


app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(notes.router,tags=["Notes"],prefix="/v1/notes")

@app.get("/")
async def home():
    """
        This is the home route.
    """
    return ["Welcome to Notes App!"]

if __name__=="__main__":
    uvicorn.run(app=app,host="0.0.0.0",port=8800)
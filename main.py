from fastapi import FastAPI
from fastapi import staticfiles
from router.post import router as post_router
from router.user import router as user_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.include_router(user_router)
app.include_router(post_router)


@app.get("/")
def home_views():
    return {"message": "Welcome to our home page"}


folder = "Post/"
app.mount("/files", StaticFiles(directory="Post"), name="file")

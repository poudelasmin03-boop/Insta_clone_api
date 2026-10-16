from fastapi import FastAPI
from fastapi import staticfiles
from router.post import router as post_router
from router.user import router as user_router
from router.comment import router as comment_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)


origin = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_origins=origin,
    allow_methods=["*"],
)


@app.get("/")
def home_views():
    return {"message": "Welcome to our home page"}


folder = "Post/"
app.mount("/files", StaticFiles(directory="Post"), name="file")

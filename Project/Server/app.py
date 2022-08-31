import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .Views.Tags import router as Tag
from .Views.Post import router as Post
from .Views.User import router as User
from .Views.Goals import router as Goals
from .Views.Recipe import router as Recipe
from .Views.Levels import router as Levels
from .Views.Workouts import router as Workout
from .Views.Exercise import router as Exercise
from .Views.Categories import router as Category
from .Views.Body_parts import router as Bodyparts
from .Views.Equipments import router as Equipments
from .Views.Subscription import router as Subscription
from .Utils.Payment import router as Razorpay

from fastapi.middleware.cors import CORSMiddleware


dir_path = os.path.dirname(os.path.realpath(__file__))
app = FastAPI()
print(dir_path,"_"*50)
app.mount("/Static", StaticFiles(directory="Project/Server"), name="Static")

IMAGEDIR=os.getcwd()
print(IMAGEDIR)
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(Workout, tags=["Workout"], prefix="/Workout")
app.include_router(User, tags=["User"], prefix="/User")
app.include_router(Exercise, tags=["Exercise"], prefix="/Exercises")
app.include_router(Bodyparts, tags=["Bodyparts"], prefix="/Bodyparts")
app.include_router(Recipe, tags=["Recipe"], prefix="/Recipe")
app.include_router(Equipments, tags=["Equipments"], prefix="/Equipments")
app.include_router(Category, tags=["Categories"], prefix="/Categories")
app.include_router(Tag, tags=["Tags"], prefix="/Tags")
app.include_router(Levels, tags=["Levels"], prefix="/Levels")
app.include_router(Goals, tags=["Goals"], prefix="/Goals")
app.include_router(Post, tags=["Post"], prefix="/Post")
app.include_router(Subscription, tags=["Subscription"], prefix="/Subscription")
app.include_router(Razorpay, tags=["Razorpay"], prefix="/Payments")


@app.get("/images", tags=["IMAGE"])
def get_images(id):
    random_index =id
    path=f"{IMAGEDIR}/{random_index}"

    print(path)
    return FileResponse(path)


@app.get("/", tags=["APP"])
def read_root():
    return {"message": dir_path}

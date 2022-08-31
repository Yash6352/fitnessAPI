from fastapi import APIRouter, Body
from bson import ObjectId
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Models.Workouts import Workout
from fastapi.encoders import jsonable_encoder
from Project.Server.Controller.Workouts import Add_Workout, Delete_Old_Image,delete_workout_data, retrieve_workout_by_id, retrieve_all_workouts, update_workout, check_title
from Project.Server.Database import Workout_collection

router = APIRouter()


@router.post("/Add_Workout", response_description="Add Workout")
async def add_workouts_data(schema: Workout = Body(...)):
    schema = jsonable_encoder(schema)
    Title = await check_title(schema['TITLE'])
    if Title == False:
        return {"code": 200, "Msg": 'Title is already Present'}
    if len(schema['IMAGE']) > 0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Workout(schema)
    return {"code": 200, "Msg": "Workout successfully added"}


@router.get("/Get_All_Workouts", response_description="Get all workout")
async def get_all_workouts():
    workout = await retrieve_all_workouts()
    if workout:
        return {"code": 200, "Data": workout}
    return {"Data": workout, "Msg": "Empty list return"}


@router.get("/Get_Workout_Data/{id}", response_description="Get workout data by id")
async def get_workouts_data(id):
    data = await retrieve_workout_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete workout data by id")
async def delete_workout(id: str):
    data = await delete_workout_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_workout_data(id: str, req: Workout):
    req = jsonable_encoder(req)
    data = {q: s for q,s in req.items() if len(str(s))!=0}
    try:
        if len(data["IMAGE"]) != 0:
            # Del_img= await Delete_Old_Image(id)
            img_path = await Image_Converter(data["IMAGE"])
            data["IMAGE"] = img_path
    except:
        pass
    updated_workout = await update_workout(id, data)
    if updated_workout:
        return {"code": 200, "Data": "Data updated Successfully"}
    return {
        "code": 404, "Data": "Something Went Wrong"
    }

@router.post("/Status/{id}" , response_description="Change workout Status")
async def Change_workout_Status(id: str):
    data = await Workout_collection.find_one({"_id":ObjectId(id)})
    if data:
        if data["STATUS"]=='Active':
            await Workout_collection.update_one({"_id":ObjectId(id)}, {"$set":{"STATUS":"Inactive"}})
        else:
            await Workout_collection.update_one({"_id":ObjectId(id)}, {"$set":{"STATUS":'Active'}})
        return {"code": 200, "Data": "Status changed Successfully"}
    return {"code": 404, "Data": "Id may not exist"}
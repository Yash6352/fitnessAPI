from fastapi import APIRouter, Body
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Controller.Exercise import Add_Exercise,Delete_Old_Image,Check_Exercises, delete_exercise_data, retrieve_all_Exercises, retrieve_exercise_by_id, update_exercise
from Project.Server.Models.Exercise import Exercise
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/Add_Exercise_Data", response_description="Add Exercise")
async def add_exercise_data(schema: Exercise = Body(...)):
    schema = jsonable_encoder(schema)
    Exercises= await Check_Exercises(schema)
    if Exercises==False:
        return {"code": 400, "Msg":"Exercise already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Exercise(schema)
    return {"code": 200, "Msg": Output}


@router.get("/Get_All_Exercises", response_description="Get all Exercises")
async def get_all_Exercises():
    workout = await retrieve_all_Exercises()
    if workout:
        return {"code": 200, "Data": workout}
    return {"Data": workout, "Msg": "Empty list return"}


@router.get("/Get_Exercise_Data/{id}", response_description="Get Exercise data by id")
async def get_exercise_data(id):
    data = await retrieve_exercise_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete Exercise data by id")
async def delete_exercise(id: str):
    data = await delete_exercise_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_exercise_data(id: str, req: Exercise = Body(...)):
    req = jsonable_encoder(req)
    data = {}
    for i, j in req.items():
        
        if (type(j) == str or type(j) == int) and (len(str(j)) > 0):
            data[i] = j
    if ('IMAGE' in data ) and (len(data["IMAGE"]) > 0):
        imagepath = await Image_Converter(data["IMAGE"])
        data["IMAGE"] = imagepath
    updated_exercise = await update_exercise(id, data)
    if updated_exercise:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}


import base64
import uuid
from fastapi import APIRouter, Body
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Controller.Body_Parts import Add_Bodypart,Delete_Old_Image, Check_Bodypart,delete_bodypart_data, retrieve_all_bodyparts, retrieve_bodypart_by_id, update_bodypart
from Project.Server.Models.Body_Parts import Bodyparts
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/Add_Bodyparts_Data", response_description="Add Body Part")
async def add_bodyparts_data(schema: Bodyparts = Body(...)):
    schema = jsonable_encoder(schema)
    Bodypart= await Check_Bodypart(schema)
    if Bodypart==False:
        return {"code": 200, "Msg":"Body already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Bodypart(schema)
    return {"code": 200, "Msg": Output}


@router.get("/Get_All_Bodyparts", response_description="Get all body parts")
async def get_all_bodyparts():
    bodyparts = await retrieve_all_bodyparts()
    if bodyparts:
        return {"code": 200, "Data": bodyparts}
    return {"Data": bodyparts, "Msg": "Empty list return"}


@router.get("/Get_Bodypart_Data/{id}", response_description="Get Body Part data by id")
async def get_bodypart_data(id):
    data = await retrieve_bodypart_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete Body Part data by id")
async def delete_bodypart(id: str):
    data = await delete_bodypart_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_bodypart_data(id: str, req: Bodyparts = Body(...)):
    req = jsonable_encoder(req)
    data = {}
    for i, j in req.items():

        if (type(j) == str or type(j) == int) and (len(str(j)) > 0):
            data[i] = j

    if "IMAGE" in data:
        if len(data["IMAGE"]) != 0:
            # Del_img= await Delete_Old_Image(id)
            imagepath = await Image_Converter(data["IMAGE"])
            data["IMAGE"] = imagepath
    updated_bodypart = await update_bodypart(id, data)
    if updated_bodypart:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }

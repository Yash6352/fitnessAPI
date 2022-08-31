import base64
import uuid
from fastapi import APIRouter, Body
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Controller.Equipments import Add_Equipment,Delete_Old_Image,Check_Eqipment, delete_equipment_data, retrieve_all_Equipments, retrieve_Equipment_by_id, update_Equipment
from Project.Server.Models.Equipments import Equipments
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/Add_Equipments_Data", response_description="Add Equipment")
async def add_Equipments_data(schema: Equipments = Body(...)):
    schema = jsonable_encoder(schema)
    Equipment = await Check_Eqipment(schema)
    if Equipment==False:
        return {"code": 200, "Msg":"Equipments already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Equipment(schema)
    return {"code": 200, "Msg": Output}


@router.get("/Get_All_Equipments", response_description="Get all Equipments")
async def get_all_Equipments():
    Equipments = await retrieve_all_Equipments()
    if Equipments:
        return {"code": 200, "Data": Equipments}
    return {"Data": Equipments, "Msg": "Empty list return"}


@router.get("/Get_Equipment_Data/{id}", response_description="Get Equipment data by id")
async def get_Equipment_data(id):
    data = await retrieve_Equipment_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete Equipment data by id")
async def delete_Equipment(id: str):
    data = await delete_equipment_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_Equipment_data(id: str, req: Equipments = Body(...)):
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
    updated_Equipment = await update_Equipment(id,data)
    if updated_Equipment:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }

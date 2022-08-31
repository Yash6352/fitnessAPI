import base64
import uuid
from fastapi import APIRouter, Body
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Controller.Categories import Add_Category,Delete_Old_Image,Check_Categories, delete_Category_data, retrieve_all_Categories, retrieve_Category_by_id, update_Category
from Project.Server.Models.Categories import Categories
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/Add_Categories_Data", response_description="Add Category")
async def add_Categories_data(schema: Categories = Body(...)):
    schema = jsonable_encoder(schema)
    Category=  await Check_Categories(schema)
    if Category==False:
        return {"code":200,"Msg":"Categories already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Category(schema)
    return {"code": 200,"Msg":Output }


@router.get("/Get_All_Categories",response_description="Get all Categories")
async def get_all_Categories():
    Categories = await retrieve_all_Categories()
    if Categories:
        return {"code": 200,"Data":Categories}
    return {"Data":Categories,"Msg":"Empty list return"}

@router.get("/Get_Category_Data/{id}",response_description="Get Category data by id")
async def get_Category_data(id):
    data = await retrieve_Category_by_id(id)
    if data:
        return {"code": 200,"Data":data}
    return {"Msg":"Id may not exist"}

@router.delete("/Delete/{id}",response_description="Delete Category data by id")
async def delete_Category(id:str):
    data = await delete_Category_data(id)
    if data:
        return {"code": 200,"Msg":data}
    return {"Msg":"Id may not exist"}

@router.put("/Update/{id}")
async def update_Category_data(id: str, req: Categories = Body(...)):
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
    updated_Category = await update_Category(id,data)
    if updated_Category:
        return {"code": 200,"Data":"Data updated Successfully"}

    return {
        "code": 404,"Data":"Something Went Wrong"
    }


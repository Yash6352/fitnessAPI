from fastapi import APIRouter, Body
from Project.Server.Database import Recipes_collection
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Controller.Recipe import Add_Recipe,Delete_Old_Image,Check_Recipe, delete_Recipes_data, retrieve_all_Recipess, retrieve_Recipes_by_id, update_Recipes
from Project.Server.Models.Recipe import Recipe
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/Add_Recipe_Data", response_description="Add Recipe")
async def add_recipe_data(schema:  Recipe = Body(...)):
    schema = jsonable_encoder(schema)
    Recipes=await Check_Recipe(schema)
    if Recipes==False:
        return { "code":200,"Msg":"Recipe already exists"}
    if len(schema['IMAGE'])>0:
        img_path=await Image_Converter(schema['IMAGE'])
    else:
        img_path=""
    schema['IMAGE'] = str(img_path)
    Output = await Add_Recipe(schema)
    return {"code": 200, "Msg": Output}


@router.get("/Get_All_Recipe", response_description="Get all Recipe")
async def get_all_Recipe():
    Recipe = await retrieve_all_Recipess()
    if Recipe:
        return {"code": 200, "Data": Recipe}
    return {"Data": Recipe, "Msg": "Empty list return"}


@router.get("/Get_Recipe_Data/{id}", response_description="Get Recipe data by id")
async def get_recipe_data(id):
    data = await retrieve_Recipes_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete Recipe data by id")
async def delete_recipe(id: str):
    data = await delete_Recipes_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_Recipe_data(id: str, req: Recipe = Body(...)):
    req = jsonable_encoder(req)
    flags=0
    data = {}
    for i, j in req.items():
        
        if (type(j) == str or type(j) == int) and (len(str(j)) > 0):
            data[i] = j

    if 'IMAGE' in data:
        if len(data["IMAGE"]) != 0:
            # Del_img= await Delete_Old_Image(id)
            imagepath = await Image_Converter(data["IMAGE"])
            data["IMAGE"] = imagepath
    updated_Recipe = await update_Recipes(id, data)
    if updated_Recipe:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {
        "code": 404, "Data": "Something Went Wrong"
    }


@router.post("/Status/{id}", response_description="Change Status of Recipe")
async def Change_Recipe_Status(id: str):
    data = await Recipes_collection.find_one({"_id":ObjectId(id)})
    if data:
        if data['STATUS'] =="Active":
            await Recipes_collection.update_one({"_id":ObjectId(id)},{"$set":{"STATUS":"Inactive"}})
        else:
            await Recipes_collection.update_one({"_id":ObjectId(id)},{"$set":{"STATUS":"Active"}})
        return {"code": 404, "Data": "Something Went Wrong"}
    return {"code": 404, "Data": "Id may not exist"}
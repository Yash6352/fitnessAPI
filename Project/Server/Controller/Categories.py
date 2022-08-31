from Project.Server.Database import *
import os
IMAGEDIR=os.getcwd()
def Categories_helper(data)-> dict:
    return {
            "_id":str(data["_id"]),
            "TITLE":data["TITLE"],
            "IMAGE": data["IMAGE"],
    }
async def Check_Categories(schema: dict):
    try :
        Title = await Categories_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else:
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Categories_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Category(schema: dict) -> dict:

        Title = await Categories_collection.insert_one(schema)
        return "Category Successfully added"

async def retrieve_all_Categories():
    Categories = []
    async for data in Categories_collection.find():
        Categories.append(Categories_helper(data))
    return Categories

async def retrieve_Category_by_id(Category_id:str) ->dict:
    Categories = await Categories_collection.find_one({"_id":ObjectId(Category_id)})
    if Categories:
        return Categories_helper(Categories)

async def delete_Category_data(id: str):
    data = await Categories_collection.find_one({"_id":ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Categories_collection.delete_one({"_id":ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"

async def update_Category(id: str, data: dict):
    if len(data) < 1:
        return False
    Category = await Categories_collection.find_one({"_id": ObjectId(id)})

    if Category:
        updated_Category = await Categories_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Category:
            return True
        return False
from Project.Server.Database import *
import os
IMAGEDIR=os.getcwd()

def Levels_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "RATE": data["RATE"],
        "IMAGE": data["IMAGE"],
    }
async def Check_Level(schema: dict):
    try:
        Title = await Levels_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else:
            return True
    except:
        return True
async def Delete_Old_Image(id:str):
        image= await Levels_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Level(schema: dict) -> dict:

        Title = await Levels_collection.insert_one(schema)
        return "Level Successfully added"


async def retrieve_all_Levels():
    Levels = []
    async for data in Levels_collection.find():
        Levels.append(Levels_helper(data))
    return Levels


async def retrieve_Level_by_id(Level_id: str) -> dict:
    Levels = await Levels_collection.find_one({"_id": ObjectId(Level_id)})
    if Levels:
        return Levels_helper(Levels)


async def delete_Level_data(id: str):
    data = await Levels_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Levels_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Level(id: str, data: dict):
    if len(data) < 1:
        return False
    Level = await Levels_collection.find_one({"_id": ObjectId(id)})
    if Level:
        updated_Level = await Levels_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Level:
            return True
        return False

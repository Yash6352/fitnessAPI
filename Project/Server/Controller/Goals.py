from Project. Server.Database import *
import os
IMAGEDIR=os.getcwd()

def Goals_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "DESCRIPTION": data["DESCRIPTION"],
        "IMAGE": data["IMAGE"],
    }
async def Check_Goal(schema: dict):
    try:
        Title = await Goals_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else:
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Goals_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path


async def Add_Goal(schema: dict) -> dict:
        Title = await Goals_collection.insert_one(schema)
        return "Goal Successfully added"


async def retrieve_all_Goals():
    Goals = []
    async for data in Goals_collection.find():
        Goals.append(Goals_helper(data))
    return Goals


async def retrieve_Goal_by_id(Goal_id: str) -> dict:
    Goals = await Goals_collection.find_one({"_id": ObjectId(Goal_id)})
    if Goals:
        return Goals_helper(Goals)


async def delete_Goal_data(id: str):
    data = await Goals_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Goals_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Goal(id: str, data: dict):
    if len(data) < 1:
        return False
    Goal = await Goals_collection.find_one({"_id": ObjectId(id)})

    if Goal:
        updated_Goal = await Goals_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Goal:
            return True
        return False

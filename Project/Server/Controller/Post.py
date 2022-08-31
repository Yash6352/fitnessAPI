from Project.Server.Database import *
import os
IMAGEDIR=os.getcwd()

def Post_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        'TAG': data["TAG"],
        'FEATURED': data["FEATURED"],
        'STATUS': data["STATUS"],
        "IMAGE": data["IMAGE"],
    }

def Single_Post_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        'DESCRIPTION': data["DESCRIPTION"],
        'TAG': data["TAG"],
        'FEATURED': data["FEATURED"],
        'STATUS': data["STATUS"],
        "IMAGE": data["IMAGE"],
    }

async def Check_Post(schema: dict):
    try:
        Title = await Post_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else:
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Post_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Post(schema: dict) -> dict:
        Title = await Post_collection.insert_one(schema)
        return "Post Successfully added"


async def retrieve_all_Post():
    Post = []
    async for data in Post_collection.find():
        Post.append(Post_helper(data))
    return Post


async def retrieve_Post_by_id(Post_id: str) -> dict:
    Post = await Post_collection.find_one({"_id": ObjectId(Post_id)})
    if Post:
        return Single_Post_helper(Post)


async def delete_Post_data(id: str):
    data = await Post_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        await Post_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Post(id: str, data: dict):
    if len(data) < 1:
        return False
    Post = await Post_collection.find_one({"_id": ObjectId(id)})
    if Post:
        updated_Post = await Post_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Post:
            return True
        return False

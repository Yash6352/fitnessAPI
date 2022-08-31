from Project.Server.Database import *

def Tags_helper(data)-> dict:
    return {
            "_id":str(data["_id"]),
            "TITLE":data["TITLE"],
    }

async def Add_Tag(schema: dict) -> dict:
    
    try :
        Title = await Tags_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return "Tag is  already in the collection"
        else:
            Title = await Tags_collection.insert_one(schema)
            return "Tag Successfully added"
    except:
        Title = await Tags_collection.insert_one(schema)
        return "Tag Successfully added"

async def retrieve_all_Tags():
    Tags = []
    async for data in Tags_collection.find():
        Tags.append(Tags_helper(data))
    return Tags

async def retrieve_Tag_by_id(Tag_id:str) ->dict:
    Tags = await Tags_collection.find_one({"_id":ObjectId(Tag_id)})
    if Tags:
        return Tags_helper(Tags)

async def delete_Tag_data(id: str):
    data = await Tags_collection.find_one({"_id":ObjectId(id)})
    if data:
        await Tags_collection.delete_one({"_id":ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"

async def update_Tag(id: str, data: dict):
    if len(data) < 1:
        return False
    Tag = await Tags_collection.find_one({"_id": ObjectId(id)})
    if Tag:
        updated_Tag = await Tags_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Tag:
            return True
        return False
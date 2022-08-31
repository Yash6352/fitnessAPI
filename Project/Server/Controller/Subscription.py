from Project.Server.Database import *
import os
IMAGEDIR=os.getcwd()

def Subscriptions_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "NAME": str(data["NAME"]),
        'DURATION': data["DURATION"],
        'DESCRIPTION': data["DESCRIPTION"],
        "PRICE": data["PRICE"],
        "STATUS": data["STATUS"],
        "IMAGE": data["IMAGE"],
    }

async def Check_Subscriptions(schema:dict):
    try:
        NAME = await Subscription_collection.find_one({"NAME": schema["NAME"]})
        if NAME:
            return False
        else:
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Subscription_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Subscriptions(schema: dict) -> dict:
        Subscriptions = await Subscription_collection.insert_one(schema)
        return "Subscriptions Successfully added"


async def retrieve_all_Subscriptions():
    Recipes = []
    async for data in Subscription_collection.find():
        Recipes.append(Subscriptions_helper(data))
    return Recipes


async def retrieve_Subscriptions_by_id(Recipes_id: str) -> dict:
    Recipes = await Subscription_collection.find_one({"_id": ObjectId(Recipes_id)})
    if Recipes:
        return Subscriptions_helper(Recipes)
    else:
        return "No Recipes found by this id"


async def delete_Subscriptions_data(id: str):
    data = await Subscription_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delte = await Delete_Old_Image(id)
        await Subscription_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Subscriptions(id: str, data: dict):
    if len(data) < 1:
        return False
    Subscriptions = await Subscription_collection.find_one({"_id": ObjectId(id)})

    if Subscriptions:
        updated_Subscriptions = await Subscription_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Subscriptions:
            return True
        return False

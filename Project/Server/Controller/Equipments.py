from Project.Server.Database import *
import os
IMAGEDIR=os.getcwd()

def Equipments_helper(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "TITLE": data["TITLE"],
        "IMAGE": data["IMAGE"],
    }

async def Check_Eqipment(schema: dict):
    try:
        Title = await Equipments_collection.find_one({"TITLE": schema["TITLE"]})
        if Title:
            return False
        else:
            return True
    except:
        return True

async def Delete_Old_Image(id:str):
        image= await Equipments_collection.find_one({"_id":ObjectId(id)})
        try:
            Del_Img=str(image["IMAGE"]).split('%2F')
            Path=str(IMAGEDIR)+chr(92)+"Server"+chr(92)+"Static"+chr(92)+ str(Del_Img[-1]).replace('/',chr(92))
            os.remove(Path)
        except:
            return "Error Ocured"
        return Path

async def Add_Equipment(schema: dict) -> dict:
        Title = await Equipments_collection.insert_one(schema)
        return "Equipment Successfully added"


async def retrieve_all_Equipments():
    Equipments = []
    async for data in Equipments_collection.find():
        Equipments.append(Equipments_helper(data))
    return Equipments


async def retrieve_Equipment_by_id(Equipment_id: str) -> dict:
    Equipments = await Equipments_collection.find_one({"_id": ObjectId(Equipment_id)})
    if Equipments:
        return Equipments_helper(Equipments)




async def add_data(id:str, data:list):
    await Exercise_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"EQUIPMENT" : data}}
        )

async def update_workout(id: str, data: list):
    await Workout_collection.update_one({"_id": ObjectId(id)}, {"$set": {"EQUIPMENT" : data}})


async def delete_equipment_data(id: str):
    data = await Equipments_collection.find_one({"_id": ObjectId(id)})
    if data:
        # Img_delete = await Delete_Old_Image(id)
        async for exercise in Exercise_collection.find():
            exercise_id= str(exercise['_id'])
            exercise_data= exercise['EQUIPMENT']
            if id in exercise_data:
                exercise_data.remove(id)
                await add_data(exercise_id, exercise_data)
        async for workout in Workout_collection.find():
            workout_id= str(workout['_id'])
            workout_data= workout['EQUIPMENT']
            if id in workout_data:
                workout_data.remove(id)
                await update_workout(workout_id, workout_data)

        await Equipments_collection.delete_one({"_id": ObjectId(id)})
        return "Data Successfully deleted"
    return "Data Not Found"


async def update_Equipment(id: str, data: dict):
    if len(data) < 1:
        return False
    Equipment = await Equipments_collection.find_one({"_id": ObjectId(id)})

    if Equipment:
        updated_Equipment = await Equipments_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_Equipment:
            return True
        return False

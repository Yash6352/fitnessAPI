from datetime import timedelta
from sys import flags
from bson import ObjectId
from fastapi import APIRouter, Body
from Project.Server.Controller.Exercise import Exercise_helper
from Project.Server.Controller.Workouts import update_workout, workout_helper
from Project.Server.Models.Workouts import Workout
from Project.Server.Utils.Image_Handler import Image_Converter
from Project.Server.Utils.Auth_Bearer import *
from Project.Server.Database import (
    Exercise_collection,
    User_collection,
    Workout_collection,
)
from Project.Server.Controller.User import User_helper, update_user
from Project.Server.Controller.User import (
    Add_User_Measures,
    Update_Measurments,
    retrieve_user_measurment,
    Add_User_Details,
    Delete_Old_Image,
    Check_Email_Mobile,
    retrieve_all_Users,
    delete_user_data,
    retrieve_user_by_id,
)
from fastapi.encoders import jsonable_encoder
from Project.Server.Models.User import (
    User_Details,
    Add_Measurment,
    Login,
    ChangePassword,
    update_users
)

router = APIRouter()


@router.post("/User_Registration", response_description="User Registration")
async def User_Registration(data: User_Details = Body(...)):
    data = jsonable_encoder(data)
    Email = await Check_Email_Mobile(data)
    if Email == False:
        return {"code": 400, "Msg": "Email or Mobile Already Registered"}
    if len(data["IMAGE"]) > 0:
        img_path = await Image_Converter(data["IMAGE"])
    else:
        img_path = ""
    data["IMAGE"] = str(img_path)
    data["PassWord"] = get_password_hash(data["PassWord"])
    Output = await Add_User_Details(data)
    return {"code": 200, "User_id": Output["_id"]}


@router.get("/Get_All_Users", response_description="Get all User Details")
async def get_all_Users():
    workout = await retrieve_all_Users()
    if workout:
        return {"code": 200, "Data": workout}
    return {"Data": workout, "Msg": "Empty list return"}


@router.get(
    "/Get_User_Data/{id}", response_description="Get user information data by id"
)
async def get_user_data(id):
    data = await retrieve_user_by_id(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.delete("/Delete/{id}", response_description="Delete user data by id")
async def delete_User(id: str):
    data = await delete_user_data(id)
    if data:
        return {"code": 200, "Msg": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_user_data(id: str, req: update_users):
    req = jsonable_encoder(req)
    data = {}
    for i, j in req.items():

        if (type(j) == str or type(j) == int) and (len(str(j)) > 0):
            data[i] = j
        if (type(j) ==list):
            data[i] =j

    if "IMAGE" in data:
        if len(data["IMAGE"]) != 0:
            # Del_img= await Delete_Old_Image(id)
            imagepath = await Image_Converter(data["IMAGE"])
            data["IMAGE"] = imagepath

    updated_user = await update_user(id, data)
    if updated_user:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}


@router.post("/Status/{id}", response_description="Change Status")
async def Change_Status(id: str):
    data = await User_collection.find_one({"_id": ObjectId(id)})
    if data:
        if data["Status"] == "Active":
            await User_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"Status": "Inactive"}}
            )
        else:
            await User_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"Status": "Active"}}
            )
        return {"code": 200, "Msg": "Status Changed Successfully"}
    return {"code": 404, "Msg": "Id may not exist"}


@router.post("/Login/", response_description="Login User")
async def login(User: Login = Body(...)):
    user = jsonable_encoder(User)
    if user["Social"] == True:
        users = await User_collection.find_one({"Mobile": (user["Email"])})
    try:
        int(user["Email"])
        users = await User_collection.find_one({"Mobile": int(user["Email"])})
    except:
        users = await User_collection.find_one({"Email": user["Email"]})
        # mobiles = await user_collection.find_one({"mobile": user['email']})
    if users and user["Social"] == True:
        access_token = create_access_token(
            data={"sub": user["Email"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "_id": str(users["_id"]),
            "name": users["Name"],
        }
    if users:
        if verify_password(user["PassWords"], users["PassWord"]):
            access_token = create_access_token(
                data={"sub": users["Email"]},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            return {
                "code": 200,
                "access_token": access_token,
                "token_type": "bearer",
                "_id": str(users["_id"]),
                "name": users["Name"],
            }
        else:
            return {"code": 404, "message": "Password not match"}
    return {"code": 404, "message": "User not found or invalid Details"}


@router.post("/Change_Password/{id}", response_description="Change the password")
async def change_password(id: str, User: ChangePassword = Body(...)):
    User = jsonable_encoder(User)
    data = await User_collection.find_one({"_id": ObjectId(id)})
    print(User["old_passWords"])
    if verify_password(User["old_passWords"], data["PassWord"]):
        data["PassWord"] = get_password_hash(User["new_password"])
        status = await User_collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return {"code": 200, "message": "Password changed successfully"}
    else:
        return {"code": 404, "message": "Please enter Valid Old Password"}


@router.post("/Add_Measurment/{id}", response_description="Add Measurment")
async def add_measurment(id: str, Measurment: Add_Measurment = Body(...)):
    data = jsonable_encoder(Measurment)
    data["User_id"] = str(id)
    status = await Add_User_Measures(data)
    return {"code": 200, "message": "Measurment added successfully"}


@router.get("/Get_Measurment/{id}", response_description="Get Measurment")
async def Get_Measurment(id: str):
    data = await retrieve_user_measurment(id)
    if data:
        return {"code": 200, "Data": data}
    return {"Msg": "Id may not exist"}


@router.put("/Update/{id}")
async def update_user_data(id: str, req: update_users):
    req = jsonable_encoder(req)
    data = {}
    for i, j in req.items():

        if (type(j) == str or type(j) == int) and (len(str(j)) > 0):
            data[i] = j
        if (type(j) == list):
            data[i] = j
    if "IMAGE" in data:
        if len(data["IMAGE"]) != 0:
            # Del_img= await Delete_Old_Image(id)
            imagepath = await Image_Converter(data["IMAGE"])
            data["IMAGE"] = imagepath

    updated_user = await update_user(id, data)
    if updated_user:
        return {"code": 200, "Data": "Data updated Successfully"}

    return {"code": 404, "Data": "Something Went Wrong"}


@router.get("/Get_User_Workout/{id}", response_description="Get user workout")
async def Get_user_workout(id: str):
    user = await User_collection.find_one({"_id": ObjectId(id)})
    user = User_helper(user)
    if user:
        workout_list = user["Workout"]
        output = []
        for each_workout in workout_list:
            workout = await Workout_collection.find_one({"_id": ObjectId(each_workout)})
            if workout:
                workout = workout_helper(workout)
                output.append(workout)
        return {"code": 200, "Data": output}
    else:
        return {"code": 404, "Data": "User not found"}


@router.get("/Calculate_BMI/{id}", response_description="Calculate BMI")
async def Get_Calculate_BMI(id: str):
    data = await retrieve_user_by_id(id)
    meter = data["Height"] / 100
    BMI = (data["Weight"]) / (meter * meter)
    return {"code": 200, "Msg": BMI}


@router.post("/FAT_CALCULATOR/{id}", response_description="FAT_CALCULATOR")
async def FAT_CALCULATOR(id:str):
    data = await retrieve_user_by_id(id)
    if data and  (data["Height"] != 0 and data["Weight"] != 0):
            height = data["Height"] / 100
            BMI = data["Weight"] / (height * height)
            age=data["Age"]
            sex=data["Gender"]
            if sex=="Male":
                body_fat= (1.20 * BMI) + (0.23 * age) - 5.4 
                return {"code": 200, "BMI": body_fat}
            else:
                body_fat= (1.20 * BMI) + (0.23 * age) - 16.2
                return {"code": 200, "BMI": body_fat}

    return {"code":404,"Data": "Something Went Wrong"}

@router.get("/User_Exercise/{id}", response_description="Get user Exercise Details")
async def get_user_exercise_details(id):
    try:
        user = await User_collection.find_one({"_id": ObjectId(id)})
        user = User_helper(user)
        if user is not None:
            workout_list = user["Workout"]
            output = []
            for each_workout in workout_list:
                if len(each_workout) > 0:
                    workout = await Workout_collection.find_one(
                        {"_id": ObjectId(each_workout)}
                    )
                    workout = workout_helper(workout)
                    if workout is not None:
                        for Day in range(1, 8):
                            DAY = "DAY_" + str(Day)
                            if len(workout[DAY]) > 0:
                                for excrcise_id in workout[DAY]:
                                    if len(excrcise_id) > 1:
                                        Exercise = await Exercise_collection.find_one(
                                            {"_id": ObjectId(excrcise_id)}
                                        )
                                        output.append(Exercise_helper(Exercise))
            if len(output) == 0:
                return {
                    "code": 200,
                    "msg": "Not any workout assigned contact administration",
                }
            return {"code": 200, "msg": output}
        else:
            return {"code": 400, "msg": "user not found"}

    except Exception as e:
        return {"code": 404, "Data": "Something Went Wrong", "msg": e.args}

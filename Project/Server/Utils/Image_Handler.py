import base64
import json
import uuid

import requests


# async def Image_Converter(Hax_Value):
#     random_name = str(uuid.uuid4())
#     decodeit = open(f"Project/Server/Static/{random_name}.jpg", 'wb')
#     decodeit.write(base64.b64decode(Hax_Value))
#     decodeit.close()
#     img_path = "http://localhost:8000/images?id=Server%2FStatic%2F" + \
#         str(random_name)+".jpg"
#     # print(random_name)
#     return img_path

async def Image_Converter(Hax_Value):
    url="https://evenmore.co.in/API/image"
    correct_payload = {"base64Image": Hax_Value, "imageName": str(uuid.uuid4())}
    json_object = json.dumps(correct_payload, indent = 4) 
    data = requests.post(url, data=json_object,headers={'Content-Type':'application/json'})
    try:
        data=data.text
        data_list=data.split('":"')
        return data_list[-1][:len(data_list[-1])-2]
    except:
        return ""


async def delete_image(path):
    url='https://evenmore.co.in/API/DeleteImage'
    correct_payload={
    "imageName":path
    }
    json_object = json.dumps(correct_payload, indent = 4) 
    requests.post(url, data=json_object,headers={'Content-Type':'application/json'})
  
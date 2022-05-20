import os
import shutil
from keras.preprocessing import image
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from zipfile import ZipFile
from flwr.common.parameter import parameters_to_weights

from preprocess_model import vgg_model, load_last_global_model_weights

class_type = {0: 'Covid', 1: 'Normal'}

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predictCovid")
async def predict(file: UploadFile = File(...)):
    def get_img_array(img):
        img = image.img_to_array(img) / 255
        img = np.expand_dims(img, axis=0)

        return img

    # img=base64.b64decode(file)
    image_name = 'img.' + str(file.filename).split(".")[-1]
    with open(image_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    img = image.load_img(image_name, target_size=(224, 224, 3))
    model = vgg_model()
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    weights = parameters_to_weights(load_last_global_model_weights( f'./../fl_sessions')[0])

    model.set_weights(weights)

    img = get_img_array(img)

    res = class_type[np.argmax(model.predict(img))]
    os.remove(image_name)
    print(res)
    return res


@app.post("/Contribute")
def contribute(file: UploadFile = File(...)):
    with open("file.zip", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    path = "/home/fawaz/Desktop/FL_dataset/test/"
    with ZipFile('file.zip', 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        zipObj.extractall(path)
        os.remove('file.zip')

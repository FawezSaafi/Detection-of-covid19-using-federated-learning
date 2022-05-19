import numpy as np
from fastapi import FastAPI, File

from fastapi.middleware.cors import CORSMiddleware
from zipfile import ZipFile

#from client.preprocess_model import vgg_model, load_last_global_model_weights

class_type = {0: 'Covid', 1: 'Normal'}

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/predictCovid")
def predict(file :bytes =File(...)) :
    print(file)
    return True
    def get_img_array(img):
        """
        Input : Takes in image path as input
        Output : Gives out Pre-Processed image
        """

        img = img.resize(224, 224, 3)
        img = img.img_to_array(img) / 255
        img = np.expand_dims(img, axis=0)

        return img

    model = vgg_model()

    model.set_weights(load_last_global_model_weights(model, f'./../fl_sessions'))

    img = get_img_array(input_data)

    res = class_type[np.argmax(model.predict(img))]

    return res
@app.post("/Contribute")
def contribute(file):
    path = ""
    with ZipFile('sampleDir.zip', 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        zipObj.extractall(path)

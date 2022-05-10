import json
import os

import flwr as fl
import numpy as np

import argparse
import sys
import warnings

# from fastapi import FastAPI


from preprocess_model import vgg_model, preprocess

if not sys.warnoptions:
    warnings.simplefilter("ignore")
parser = argparse.ArgumentParser(description='Test.')
parser.add_argument('--client', action='store', type=int, help='client number')
parser.add_argument('--id', action='store', type=int, help='client number')
parser.add_argument('--@ip', action='store', type=str, help='ip-address')
parser.add_argument('--port', action='store', type=int, help='client port')
parser.add_argument('--path', action='store', type=str, help='path of the client dataset')



args = parser.parse_args()
client_id ,  ip_address , port, data_path = vars(args)['id'],vars(args)['@ip'],vars(args)['port'],vars(args)['path']

# app = FastAPI()

# @app.post("/participateFL")
# def listen_and_participate (train_start:int, train_end:int, ipadress:str, port:int):


class_type = {0:'Covid',  1 : 'Normal'}
model = vgg_model()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
data_path=data_path+str(client_id)+"/"
# Define Flower client
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model , client_id):
        # init the datasets to be used and the model architecture
        self.model=model

        self.client_id=client_id

    def get_parameters(self):
        return self.model.get_weights()

    def fit(self, parameters, config):
        session = config["session"]
        self.model.set_weights(parameters)
        global train, test, valid
        train, test, valid = preprocess(data_path, str(client))
        with open('model_config.json', 'r') as model_config:
            config_data = model_config.read()
            model_data = json.loads(config_data)
        hist = self.model.fit_generator(train, steps_per_epoch=model_data['steps_per_epoch'], epochs=model_data['epochs'], validation_data=valid, validation_steps=model_data['validation_steps'])
        params = self.model.get_weights()

        if not (os.path.exists(f'./Local-weights')):
            os.mkdir(f"./Local-weights")

        if not (os.path.exists(f'./Local-weights/Session-{session}')):
            os.mkdir(f"./Local-weights/Session-{session}")

        # Save training weights in the created directory
        filename = f'./Local-weights/Session-{session}/Round-{str(config["rnd"])}-training-weights.npy'
        np.save(filename, params)
        results = {
            "loss": hist.history["loss"][0],
            "accuracy": hist.history["accuracy"][0],
            #"val_loss": hist.history["val_loss"][0],
            #"val_accuracy": hist.history["val_accuracy"][0],
        }
        return self.model.get_weights(), len(train), results

    def evaluate(self, parameters, config):

        self.model.set_weights(parameters)
        loss, accuracy = model.evaluate_generator(test)
        print('loss :', loss, 'accuracy : ', accuracy)
        return loss, len(test), {"accuracy": accuracy}


# start Flower client
    # fl.client.start_numpy_client(
    #     server_address=args.ipadress + ":" + str(args.port),
    #     client=FlowerClient(),
    #     grpc_max_message_length=1024 * 1024 * 1024,
    # )
client = FlowerClient(model,client_id)
fl.client.start_numpy_client(ip_address+":"+str(port), client=client)

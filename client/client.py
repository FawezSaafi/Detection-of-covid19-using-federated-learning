
import flwr as fl
import argparse
import sys
import warnings



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
client_id, ip_address, port, data_path = vars(args)['id'], vars(args)['@ip'], vars(args)['port'], vars(args)['path']

class_type = {0: 'Covid', 1: 'Normal'}
model = vgg_model()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
data_path = data_path + str(client_id) + "/"


# Define Flower client
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, model, client_id):
        # init the datasets to be used and the model architecture
        self.model = model

        self.client_id = client_id

    def get_parameters(self):
        return self.model.get_weights()

    def fit(self, parameters, config):
        session = config["session"]
        steps_per_epoch: int = config["steps_per_epoch"]
        epochs: int = config["epochs"]
        validation_steps = config["validation_steps"]
        self.model.set_weights(parameters)
        global train, test, valid
        train, test, valid = preprocess(data_path, str(client))

        hist = self.model.fit_generator(train, steps_per_epoch=steps_per_epoch, epochs=epochs, validation_data=valid,
                                        validation_steps=validation_steps)
        params = self.model.get_weights()

        results = {
            "loss": hist.history["loss"][0],
            "accuracy": hist.history["accuracy"][0],
            # "val_loss": hist.history["val_loss"][0],
            # "val_accuracy": hist.history["val_accuracy"][0],
        }
        return self.model.get_weights(), len(train), results

    def evaluate(self, parameters, config):
        steps: int = config["val_steps"]

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
client = FlowerClient(model, client_id)
fl.client.start_numpy_client(ip_address + ":" + str(port), client=client)

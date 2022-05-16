import argparse
import time

from keras.applications import vgg16
from keras_preprocessing.image import ImageDataGenerator
import json

from FLstrategies import *

# from fastapi.middleware.cors import CORSMiddleware


parser = argparse.ArgumentParser(description='Test.')
parser.add_argument('--rounds', action='store', type=int, help='number of rounds')
parser.add_argument('--@ip', action='store', type=str, help='ip address')
parser.add_argument('--port', action='store', type=int, help='port')
parser.add_argument('--resume', action='store', type=bool, help='resume from the previous weights')
parser.add_argument('--test_path', action='store', type=str, help='test data to do a server-side evaluation')
args = parser.parse_args()
num_rounds, ipaddress, port, resume, test_path = vars(args)["rounds"], vars(args)["@ip"], vars(args)["port"], \
                                                 vars(args)["resume"], vars(args)['test_path']


def launch_fl_session(num_rounds: int, ipaddress: str, port: int, resume: bool):
    """
    """
    session = str(time.time())
    with open('config_training.json', 'r+') as file:
        config = json.load(file)
        data = {'num_rounds': num_rounds, "resume": resume, "session": session}
        config["session_details"].append(data)
        file.seek(0)
        json.dump(config, file, indent=4)

    # Load last session parameters if they exist
    if not (os.path.exists('../fl_sessions')):
        # create fl_sessions directory if first time
        os.mkdir('../fl_sessions')

        # initialise sessions list and initial parameters
    sessions = []
    initial_params = None

    for root, dirs, files in os.walk("../fl_sessions", topdown=False):
        for name in dirs:
            if name.find('Session') != -1:
                sessions.append(name)

    if (resume and len(sessions) != 0):
        # test if we will start def get_eval_fn(model):
        # if we have at least a session directory
        if os.path.exists(f'./fl_sessions/{sessions[-1]}/global_session_model.npy'):
            # if the latest session directory contains the global model parameters
            initial_parameters = np.load(f"./fl_sessions/{sessions[-1]}/global_session_model.npy", allow_pickle=True)
            initial_params = initial_parameters[0]
            # load latest session's global model parameters
    with open('strategy_coefs.json ', 'r') as file:
        config = json.load(file)
        data = json.dumps(config)
        data = json.loads(data)
        strategy_coefs = {"min available clients": data["min_available_clients"],
                          "min evaluation clients": data["min_evaluation_clients"],
                          "min fitting clients": data["min_fitting_clients"],
                          "fraction of clients for fitting": data["fraction_of_clients_for_fitting"],
                          "fraction of clients for evaluation": data["fraction_of_clients_for_evaluation"]}
    # Create strategy and run server
    strategy = SaveModelStrategy(
        fraction_fit=strategy_coefs["fraction of clients for fitting"],
        fraction_eval=strategy_coefs["fraction of clients for evaluation"],
        min_fit_clients=strategy_coefs["min fitting clients"],
        min_eval_clients=strategy_coefs["min evaluation clients"],
        min_available_clients=strategy_coefs["min available clients"],
        initial_parameters=initial_params,
        eval_fn=get_eval_fn(model),
        on_fit_config_fn=get_on_fit_config_fn(),
        on_evaluate_config_fn=evaluate_config,
    )

    fl.server.start_server(
        server_address=ipaddress + ':' + str(port),
        config={"num_rounds": num_rounds},
        grpc_max_message_length=1024 * 1024 * 1024,
        strategy=strategy
    )


def get_eval_fn(model):
    """Return an evaluation function for server-side evaluation."""
    # The `evaluate` function will be called after every round
    # steps = 0
    test_data_gen = ImageDataGenerator(preprocessing_function=vgg16.preprocess_input, rescale=1. / 255)
    test = test_data_gen.flow_from_directory(directory=test_path,
                                             target_size=(224, 224), shuffle=False)

    def evaluate(
            weights: fl.common.Weights) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
        model.set_weights(weights)
        loss, accuracy = model.evaluate_generator(test)

        with open('config_training.json', 'r') as config_training:
            config = config_training.read()
            data = json.loads(config)
            session = data["session_details"][-1]["session"]
        with open('server/evaluation.json', 'r+') as eval_file:
            config = json.load(eval_file)
            data = {session: {'global_loss': loss, 'global_accuracy': accuracy}}

            config['session'].append(data)

            eval_file.seek(0)
            json.dump(config, eval_file, indent=4)

        print('global_loss :', loss, 'global_accuracy : ', accuracy)
        # return loss, {"accuracy": accuracy}

    return evaluate


launch_fl_session(num_rounds, ipaddress, port, resume)

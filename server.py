# from fastapi import FastAPI

# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
import argparse

import flwr as fl
import numpy as np
import os
import time
from FLstrategies import *

# from blockchain_service import *
# from fastapi.middleware.cors import CORSMiddleware
parser = argparse.ArgumentParser(description='Test.')
parser.add_argument('--rounds', action='store', type=int, help='number of rounds')
parser.add_argument('--@ip', action='store', type=str, help='ip address')
parser.add_argument('--port', action='store', type=int, help='port')
parser.add_argument('--resume', action='store', type=bool, help='resume from the previous weights')
args = parser.parse_args()
num_rounds, ipaddress, port, resume = vars(args)["rounds"], vars(args)["@ip"], vars(args)["port"], vars(args)["resume"]


def launch_fl_session(num_rounds: int, ipaddress: str, port: int, resume: bool):
    """
    """
    session = int(time.time())
    with open('config_training.json', 'r+') as file:
        config = json.load(file)
        data = {'num_rounds': num_rounds, "ip-adress": ipaddress, "port": port, "resume": resume, "session": session}
        config["session_details"].append(data)
        file.seek(0)
        json.dump(config, file, indent=4)

    # Load last session parameters if they exist
    if not (os.path.exists('./fl_sessions')):
        # create fl_sessions directory if first time
        os.mkdir('fl_sessions')

        # initialise sessions list and initial parameters
    sessions = []
    initial_params = None

    for root, dirs, files in os.walk("./fl_sessions", topdown=False):
        for name in dirs:
            if name.find('Session') != -1:
                sessions.append(name)
    # loop through fl_sessions sub-folders and get the list of directories containing the weights

    if (resume and len(sessions) != 0):
        # test if we will start training from the last session weights and
        # if we have at least a session directory
        if os.path.exists(f'./fl_sessions/{sessions[-1]}/global_session_model.npy'):
            # if the latest session directory contains the global model parameters
            initial_parameters = np.load(f"./fl_sessions/{sessions[-1]}/global_session_model.npy", allow_pickle=True)
            initial_params = initial_parameters[0]
            # load latest session's global model parameters

    strategy_coefs = {"min available clients": 2,
                      "min evaluation clients": 2,
                      "min fitting clients": 2,
                      "fraction of clients for fitting": 1.0,
                      "fraction of clients for evaluation": 1.0}
    # Create strategy and run server
    strategy = SaveModelStrategy(
        fraction_fit=strategy_coefs["fraction of clients for fitting"],
        fraction_eval=strategy_coefs["fraction of clients for evaluation"],
        min_fit_clients=strategy_coefs["min fitting clients"],
        min_eval_clients=strategy_coefs["min evaluation clients"],
        min_available_clients=strategy_coefs["min available clients"],
        initial_parameters=initial_params,
        on_fit_config_fn=get_on_fit_config_fn(),
        on_evaluate_config_fn=evaluate_config,
    )

    fl.server.start_server(
        server_address=ipaddress + ':' + str(port),
        config={"num_rounds": num_rounds},
        grpc_max_message_length=1024 * 1024 * 1024,
        strategy=strategy
    )


launch_fl_session(num_rounds, ipaddress, port, resume)

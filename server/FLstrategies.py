import flwr as fl
import numpy as np
import os
from typing import Callable, Dict, Optional, Tuple
from flwr.common import Parameters, Scalar, Weights
from typing import Callable, Dict
import json
import socket

from preprocess_model import vgg_model

model = vgg_model()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

class SaveModelStrategy(fl.server.strategy.FedAvg):
    def __init__(self,
                 *,
                 fraction_fit: float = 0.1,
                 fraction_eval: float = 0.1,
                 min_fit_clients: int = 2,
                 min_eval_clients: int = 2,
                 min_available_clients: int = 2,
                 eval_fn: Optional[
                     Callable[[Weights], Optional[Tuple[float, Dict[str, Scalar]]]]
                 ] = None,
                 on_fit_config_fn: Optional[Callable[[int], Dict[str, Scalar]]] = None,
                 on_evaluate_config_fn: Optional[Callable[[int], Dict[str, Scalar]]] = None,
                 accept_failures: bool = True,
                 initial_parameters: Parameters
                 ) -> None:
        super().__init__(
            fraction_fit=fraction_fit,
            fraction_eval=fraction_eval,
            min_fit_clients=min_fit_clients,
            min_eval_clients=min_eval_clients,
            min_available_clients=min_available_clients,
            eval_fn=eval_fn,
            on_fit_config_fn=on_fit_config_fn,
            on_evaluate_config_fn=on_evaluate_config_fn,
            accept_failures=accept_failures,
            initial_parameters=initial_parameters,
        )

    def aggregate_fit(
            self,
            rnd,
            results,
            failures
    ):
        aggregated_weights: object = super().aggregate_fit(rnd, results, failures)
        if aggregated_weights is not None:

            # get num_rounds from config_training json file to be use to verify
            # if the current round is the first round
            with open('config_training.json', 'r') as config_training:
                config = config_training.read()
                data = json.loads(config)
                num_rounds = data["session_details"][-1]['num_rounds']
                session = data["session_details"][-1]['session']

            # Save aggregated_weights
            print(f"Saving round {rnd} aggregated_weights...")

            if not os.path.exists(f"./fl_sessions/Session-{session}"):
                os.makedirs(f"./fl_sessions/Session-{session}")
                #if rnd < num_rounds:
                    #np.save(f"./fl_sessions/Session-{session}/round-{rnd}-weights.npy", aggregated_weights)
            if os.path.exists(f"./fl_sessions/Session-{session}/round-weights.npy"):
                os.remove(f"./fl_sessions/Session-{session}/round-weights.npy")
                np.save(f"./fl_sessions/Session-{session}/round-weights.npy", aggregated_weights)
            else :
                np.save(f"./fl_sessions/Session-{session}/round-weights.npy", aggregated_weights)



        return aggregated_weights


# Define batch-size, nb of epochs and verbose for fitting
def get_on_fit_config_fn() -> Callable[[int], Dict[str, str]]:
    """Return a function which returns training configurations."""

    def fit_config(rnd: int) -> Dict[str, str]:
        with open('config_training.json', 'r') as config_training:
            config = config_training.read()
            data = json.loads(config)
            # print(data["session_details"][-1]["session"])
            session = data["session_details"][-1]["session"]

            with open('server/model_config.json', 'r') as model_config:
                config = model_config.read()
                model_data = json.loads(config)
                batch_size = model_data["batch_size"]
                epochs = model_data["epochs"]
                verbose = model_data["verbose"]
                steps_per_epoch = model_data['steps_per_epoch']
                validation_steps = model_data['validation_steps']


                config = {
                    "validation_steps": validation_steps,
                    "steps_per_epoch":steps_per_epoch,

                    "batch_size": batch_size,
                    "epochs": epochs,
                    "verbose": verbose,
                    "rnd": rnd,
                    "session": session
                }
        return config

    return fit_config


# Define hyper-parameters for evaluation
def evaluate_config(rnd: int):
    with open('server/model_config.json', 'r') as model_config:
        config = model_config.read()
        data = json.loads(config)

        val_steps = data["validation_steps"]
    with open('config_training.json', 'r') as config_training:
        config = config_training.read()
        data = json.loads(config)
        session = data["session_details"][-1]['session']
        config = {"val_steps": val_steps, "verbose": 0, "rnd": rnd, "session": session}
    return config


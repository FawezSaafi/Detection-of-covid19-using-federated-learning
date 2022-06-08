import json
import os
from urllib.request import Request
# from server import launch_fl_session
import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Request
import shutil

from server import launch_fl_session
import mysql.connector as MC
from datetime import datetime
import flwr as fl

conn = MC.connect(host='localhost', database='mysql', user='root', password='')

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

default_ip = "localhost"


# num_rounds:parseInt(launch.num_rounds),
# ipaddress:launch.ipaddress,
# port:parseInt(launch.port),
# resume:launch.resume


@app.post("/launchFL")
async def launch_session(fastapi_req: Request):
    body = await fastapi_req.body()
    my_json = body.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    print(data["ipaddress"])

    # return True

    # launch_fl_session(int(data["num_rounds"]), data["ipaddress"], data["port"], data["resume"])

    # os.makedirs(f'./nada')
    with open(f'./../strategy_coefs.json', 'r+') as file:
        config = json.load(file)
        config["min_available_clients"] = int(data["num_clients"])
        config["min_evaluation_clients"] = int(data["num_clients"])
        config["min_fitting_clients"] = int(data["num_clients"])
        file.seek(0)
        json.dump(config, file, indent=4)

    cursor = conn.cursor()
    req = 'select * from client'
    cursor.execute(req)
    clientlist = cursor.fetchall()
    for client in clientlist:
        # i+/=1
        print(client[0])
        reqnotif = """INSERT INTO notification (id_client, id_server, state, notif_date) VALUES (%s,%s,%s,%s)"""
        # print(cursor.lastrowid)
        infos = (client[0], 10, 0, datetime.now())
        cursor.execute(reqnotif, infos)
        conn.commit()
    launch_fl_session(int(data["num_rounds"]), data["ipaddress"], data["port"], data["resume"])

    with open(f'evaluation.json', 'r+') as file:
        config = json.load(file)
        acc = "{:.2f}".format(config["session"][-1][list(config["session"][-1].keys())[0]]["global_accuracy"])
        sess = list(config["session"][-1].keys())[0]
    reqhist = """INSERT INTO historique_server (session_date, nb_rounds, accuracy) VALUES (%s,%s,%s)"""
    infos_hist = (sess, data["num_rounds"], acc)
    cursor.execute(reqhist, infos_hist)
    conn.commit()
    print({"session": sess, "num_rnds": data["num_rounds"], "accuracy": acc})
    return {"session": sess, "num_rnds": data["num_rounds"], "accuracy": acc}


@app.get("/selectHist")
def select_hist():
    cursor = conn.cursor()
    req = 'select * from historique_server'
    cursor.execute(req)
    hist_list = cursor.fetchall()
    return hist_list
# uvicorn server_api:main --reload

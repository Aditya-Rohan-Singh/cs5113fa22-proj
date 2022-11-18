import grpc
import socket
import time
import pokemon_game_pb2_grpc
import pokemon_game_pb2
import concurrent
import json
import numpy as np


rng = np.random.default_rng()
global N

class PokemonGame(pokemon_game_pb2_grpc.PokemonGameServicer):
    def checkboard(self,request,context):
        print("blah")

def pokemon():
    print("I'm up")


def trainer():
    print("I'm up")


def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    pokemon_game_pb2_grpc.add_PokemonGameServicer_to_server(PokemonGame(),server)
    server.add_insecure_port('server:50051')
    server.start()
    with open('config.json') as json_file:
        data = json.load(json_file)
    n = data['N']
    T = data['T']
    P = data['P']
    json_file.close()
    global N
    #create board
    N = [[0]*n for _ in range(n)]
    
    #populate trainers
    idx = 0
    while idx != T:
        i = rng.integers(low=0, high=n-1, size=1)[0]
        j = rng.integers(low=0, high=n-1, size=1)[0]
        if N[i][j]==0:
            upd = 'T' + str(idx+1)
            N[i][j] = upd
            idx = idx + 1

    #populate pokemon
    idx1 = 0
    while idx1 != P:
        i = rng.integers(low=0, high=n-1, size=1)[0]
        j = rng.integers(low=0, high=n-1, size=1)[0]
        if N[i][j]==0:
            upd = 'P' + str(idx1+1)
            N[i][j] = upd
            idx1 = idx1 + 1
    display_board(n)

def display_board(n):
    global N
    with open('node-list.json') as json_file:
        data = json.load(json_file)
    for i in range(n):
        row = ""
        for j in range(n):
            if(N[i][j] == 0):
                row = row + "|__|"
            else:
                row = row + "|" + data[N[i][j]] + "|"
        print(row)
    json_file.close()


    # Try case to exit server
    try :
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    hostname = socket.gethostname()
    if socket.gethostname() == 'server':
        serve()
    else:
        hostname = hostname[:-1]
        if hostname == "trainer":
            trainer()
        elif hostname == "pokemon":
            pokemon()

import grpc
import socket
import time
import pokemon_game_pb2_grpc
import pokemon_game_pb2
import concurrent
import json

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
    N = data['N']
    T = data['T']
    P = data['P']
    print(N,T,P)
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

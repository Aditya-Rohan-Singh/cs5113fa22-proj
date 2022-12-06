import grpc
import socket
import time
import pokemon_game_pb2_grpc
import pokemon_game_pb2
import concurrent
import json
import numpy as np
import pickle

rng = np.random.default_rng()
global N, n, no_of_pokemon, lock_flag

def get_position(hostname1):
    with open('board.pickle', 'rb') as handle:
        board = pickle.load(handle)
    if(hostname1[:-1]=='trainer'):
        for i,k in enumerate(board):
            if(list(board.values())[i]['trainer'] == hostname1):
                x,y = k
                return(x,y,0)
                break;
    elif(hostname1[:-1]=='pokemon'):
        for idx,k in enumerate(board):
            if (hostname1 in list(board.values())[idx]['pokemon']):
                x,y = k
                hostname_caught = 0
                break;
            else:
                x,y =-1,-1
                hostname_caught = -1
        return(x,y,hostname_caught)

def possible_moves(i,j,hostname1):
    list_array = [[i-1,j-1], [i-1,j], [i-1,j+1], [i,j+1], [i+1,j+1], [i+1,j], [i+1,j-1], [i,j-1]]
    if(hostname1[:-1]=='pokemon'):
        pokemon_moves = [-1 if(k1 < 0 or k1 == n or k2 < 0 or k2 ==n)  else 2 if N[k1,k2]['trainer'][:-1] == 'trainer' else 0 if(len(N[k1,k2]['pokemon']) > 1) else 0 for (k1,k2) in list_array ]
    elif(hostname1[:-1]=='trainer'):
        pokemon_moves = [-1 if(k1 < 0 or k1 == n or k2 < 0 or k2 ==n)  else -1 if N[k1,k2]['trainer'][:-1] == 'trainer' else 1 if(len(N[k1,k2]['pokemon']) > 1) else 0 for (k1,k2) in list_array ]

    return(pokemon_moves)

class PokemonGame(pokemon_game_pb2_grpc.PokemonGameServicer):
    def checkboard(self,request,context):
        global no_of_pokemon
        #mov = [0]*8
        lock_flag = 1
        hostname1 = request.hostname
        old_i, old_j, caught = get_position(hostname1)
        position = [old_i,old_j]    
        no_of_pokemon = 0
        if caught != -1:
            mov = possible_moves(old_i,old_j,hostname1)
        else:
            mov = [0]*8
        return(pokemon_game_pb2.checkpos(pos_array = mov, pokemon_left = no_of_pokemon, lock = lock_flag, cur_pos = [old_i,old_j], alive = caught))

    def move(self,request,context):
        
        com = 1
        return(pokemon_game_pb2.movecompleted(status = com))

def pos_move(hostname1, position, current):
    

def pokemon():
    with grpc.insecure_channel("server:50051") as channel:
        stub = pokemon_game_pb2_grpc.PokemonGameStub(channel)
        flag = 1
        hname = socket.gethostname()
        while (flag != 0):
            response = stub.checkboard(pokemon_game_pb2.name(hostname = hname),wait_for_ready=True)
            if(response.alive == -1):
                flag = 0
            else
                flag = response.pokemon_left
                
            print(response.pos_array, response.cur_pos)

def trainer():
    with grpc.insecure_channel("server:50051") as channel:
        stub = pokemon_game_pb2_grpc.PokemonGameStub(channel)
        flag = 1
        hname = socket.gethostname()
        while (flag!=0):
            response = stub.checkboard(pokemon_game_pb2.name(hostname = hname),wait_for_ready=True)
            flag = response.pokemon_left
            if(response.alive == -1 or response.pokemon_left == 0)
                flag = 0
            else:
                flat = response.pokemon_left
            print(response.pos_array,response.cur_pos)


def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    pokemon_game_pb2_grpc.add_PokemonGameServicer_to_server(PokemonGame(),server)
    server.add_insecure_port('server:50051')
    #server.start()
    with open('config.json') as json_file:
        data = json.load(json_file)
    global n , no_of_pokemon, N, lock_flag
    n = data['N']
    T = data['T']
    P = data['P']
    no_of_pokemon = P
    json_file.close()
    
    #define file lock
    lock_flag = 0
    #create board
    N = {}

    #Initalized N dictionary
    for i in range(n):
        for j in range(n):
            N[(i,j)] = {}
            N[(i,j)]['trainer'] = ''
            N[(i,j)]['pokemon'] = []
    #add all the trainers
    idx = 0
    while idx != T:
        i = rng.integers(low=0, high=n-1, size=1)[0]
        j = rng.integers(low=0, high=n-1, size=1)[0]
        if len(N[i,j]['trainer'])==0:
            upd = 'trainer' + str(idx+1)
            N[i,j]['trainer'] = upd
            idx = idx +1

    #populate pokemon
    idx1 = 0
    while idx1 != P:
        i = rng.integers(low=0, high=n-1, size=1)[0]
        j = rng.integers(low=0, high=n-1, size=1)[0]
        #if N[i][j]==0:
        if len(N[i,j]['trainer'])==0:
            upd = 'P' + str(idx1+1)
            if len(list(N[i, j]['pokemon']))>0:
                new_list = list(N[i, j]['pokemon'])
                new_list.append('pokemon'+ str(idx1+1))
            else:
                new_list = ["pokemon" + str(idx1+1)]
            N[i, j]['pokemon'] = new_list
            idx1 = idx1 +1

    with open('board.pickle', 'wb') as handle:
        pickle.dump(N, handle, protocol=pickle.HIGHEST_PROTOCOL)
    display_board(n)
    print(N)
    server.start()
     # Try case to exit server
    try :
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        server.stop(0)

def display_board(n):
    print("function started")
    global N
    with open('node-list.json') as json_file:
        data = json.load(json_file)

    with open('board.pickle', 'rb') as handle:
        board = pickle.load(handle)
    for i2 in range(n):
        row = ""
        for j2 in range(n):
            if len(board[i2,j2]['trainer']) > 0:
                row = row + "||" + data[board[i2,j2]['trainer']]
            elif len(board[i2,j2]['pokemon']) > 0:
                row = row + "||"
                for val in list(board[i2,j2]['pokemon']):
                    row = row + data[val] + "|"
            else:
                row = row + "|__|"
        print(row)


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

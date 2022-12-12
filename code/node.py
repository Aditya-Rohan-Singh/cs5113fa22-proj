import grpc
from grpc import aio
import socket
import time
import pokemon_game_pb2_grpc
import pokemon_game_pb2
import concurrent
import json
import numpy as np
import pickle
import random
import asyncio
import logging

rng = np.random.default_rng()
global N, n, no_of_pokemon, lock_flag, pokedex, path

def get_position(hostname1):
    with open('board.pickle', 'rb') as handle:
        board = pickle.load(handle)
    if(hostname1[:-1]=='trainer'):
        for i,k in enumerate(board):
            if(list(board.values())[i]['trainer'] == hostname1):
                x,y = k
                hostname_caught = 0
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
    with open('board.pickle', 'rb') as handle:
        board = pickle.load(handle)

    if(hostname1[:-1]=='pokemon'):
        pokemon_moves = [-1 if(k1 < 0 or k1 == n or k2 < 0 or k2 ==n)  else 2 if board[k1,k2]['trainer'][:-1] == 'trainer' else 0 if(len(board[k1,k2]['pokemon']) > 1) else 0 for (k1,k2) in list_array ]
    elif(hostname1[:-1]=='trainer'):
        pokemon_moves = [-1 if(k1 < 0 or k1 == n or k2 < 0 or k2 ==n)  else -1 if board[k1,k2]['trainer'][:-1] == 'trainer' else 1 if(len(board[k1,k2]['pokemon']) > 0) else 0 for (k1,k2) in list_array ]

    return(pokemon_moves)

class PokemonGame(pokemon_game_pb2_grpc.PokemonGameServicer):
    def checkboard(self,request,context):
        global no_of_pokemon, lock_flag
        hostname1 = request.hostname
        if(lock_flag == 'server'):
            lock_flag = hostname1
            old_i, old_j, caught = get_position(hostname1)
            position = [old_i,old_j]    
            if caught != -1:
                mov = possible_moves(old_i,old_j,hostname1)
                if(no_of_pokemon==0):
                    caught = -1
                    lock_flag = 'server'
            elif caught == -1:
                mov = [0]*8
                lock_flag = 'server'
            return(pokemon_game_pb2.checkpos(pos_array = mov, pokemon_left = no_of_pokemon, lock = lock_flag, cur_pos = position, alive = caught))
        else:
            mov = [0]*8
            old_i, old_j, caught = get_position(hostname1)
            position = [old_i,old_j]
            return(pokemon_game_pb2.checkpos(pos_array = mov, pokemon_left = no_of_pokemon, lock = lock_flag, cur_pos = position, alive = caught))

    def Move(self,request,context):
        global lock_flag
        if(lock_flag==request.hostname):
            with open('board.pickle', 'rb') as handle:
                board = pickle.load(handle)
            with open('pokedex.pickle','rb') as handle:
                poked = pickle.load(handle)
            
            #update move
            if(request.hostname[:-1] == 'trainer'):
                old_i, old_j, caught = get_position(request.hostname)
                board[(old_i,old_j)]['trainer'] = ''
                board[(request.row, request.column)]['trainer']= request.hostname
                #If a capture request is sent out
                global no_of_pokemon
                if request.capture == 1:
                    if(len(list(board[(request.row,request.column)]['pokemon'])) > 0):
                        if len(poked[request.hostname]) > 0:
                            value = 0
                            for val in list(board[(request.row,request.column)]['pokemon']):
                                
                                value = value + 1
                            no_of_pokemon = no_of_pokemon - value#len(board[(request.row,request.column)]['pokemon'])
                            new_list = poked[request.hostname]
                            new_list.extend(board[(request.row,request.column)]['pokemon'])
                            poked[request.hostname] = new_list
                        else:
                            poked[request.hostname] = board[(request.row,request.column)]['pokemon']
                            no_of_pokemon = no_of_pokemon - 1 
                        board[(request.row,request.column)]['pokemon'] = []
            elif(request.hostname[:-1] == 'pokemon'):
                #Update old position without the pokemon name
                old_i, old_j, caught = get_position(request.hostname)
                pokemon_list = list(board[(old_i, old_j)]['pokemon'])
                pokemon_list.remove(request.hostname)
                board[old_i, old_j]['pokemon'] = pokemon_list
                if len(list(board[(request.row, request.column)]['pokemon'])) > 0:
                    new_list = list(board[request.row, request.column]['pokemon'])
                    new_list.append(request.hostname)
                else:
                    new_list = [request.hostname]
                board[(request.row, request.column)]['pokemon'] = new_list
                
            #updagte path 
            with open('path.pickle', 'rb') as handle:
                path = pickle.load(handle)
            if((old_i, old_j) != (request.row, request.column)):
                row = path[request.hostname]
                row.append([request.row, request.column])
                path[request.hostname] = row
            print(poked)

            with open('path.pickle', 'wb') as handle:
                pickle.dump(path, handle, protocol=pickle.HIGHEST_PROTOCOL)

            with open('pokedex.pickle','wb') as handle1:
                pickle.dump(poked, handle1,  protocol=pickle.HIGHEST_PROTOCOL)

            with open('board.pickle', 'wb') as handle2:
                pickle.dump(board, handle2, protocol=pickle.HIGHEST_PROTOCOL)
            
            global n
            display_board(n)
            lock_flag = 'server'
            com = 1
        else:
            com = 0
        return(pokemon_game_pb2.movecomplete(status = com))
    
    def pokemon_list(self,request,context):
        with open('pokedex.pickle','rb') as handle1:
            poked = pickle.load(handle1)

        pokemon_li = poked[request.hostname]
        return(pokemon_game_pb2.pokemon_captured(pokemon_name = pokemon_li))
    
    def trainer_list(self, request,contect):
        with open('pokedex.picle', 'rb') as handle:
            poked = pickle.load(handle)

        for k,v in poked.items():
            if request.hostname in list(v):
                trainer_name = k
        return(pokemon_game_pb2.trainer_name(trainer = trainer_name))

def trainer_pos_move(hostname1, pokemon_moves, current):
    moves = []
    i,j = current[0],current[1]
    list_array = [[i-1,j-1], [i-1,j], [i-1,j+1], [i,j+1], [i+1,j+1], [i+1,j], [i+1,j-1], [i,j-1]]
    capture = 0
    if 1 in pokemon_moves:
        for idx, value in enumerate(pokemon_moves):
            if(value == 1):
                moves.append(idx)
                capture = 1
    elif 0 in pokemon_moves:
        for idx, value in enumerate(pokemon_moves):
            if(value == 0):
                moves.append(idx)
    else:
        moves = []
    
    if len(moves) > 0:
        new_i, new_j = list_array[random.choice(moves)]
    else:
        new_i, new_j = i, j
    
    return(new_i, new_j, capture)

def pokemon_pos_move(hostname1, pokemon_moves, current):
    moves = []
    i,j = current[0],current[1]
    list_array = [[i-1,j-1], [i-1,j], [i-1,j+1], [i,j+1], [i+1,j+1], [i+1,j], [i+1,j-1], [i,j-1]]
    if 2 not in pokemon_moves:
        moves = []
    elif 0 in pokemon_moves:
        for idx, value in enumerate(pokemon_moves):
            if(value == 0):
                moves.append(idx)
    else:
        moves = []

    #Remove moves near trainers
    trainer_pos = []
    for idx2, pok in enumerate(pokemon_moves):
        if pok == 2:
            trainer_pos.append(idx2)
    for idx1 in trainer_pos:
        train_x, train_y = list_array[idx1]
        for idx3 in moves:
            temp_i, temp_j = list_array[idx3]
            if(abs(train_x -temp_i)<=1 or abs(train_y-temp_j)<=1):
                moves.remove(idx3)
    if len(moves) > 0:
        new_i, new_j = list_array[random.choice(moves)]
    else:
        new_i, new_j = i,j
    
    return(new_i,new_j)

async def pokemon():
    async with grpc.aio.insecure_channel("server:50051") as channel:
        stub = pokemon_game_pb2_grpc.PokemonGameStub(channel)
        flag = 1
        hname = socket.gethostname()
        while (flag != 0):
            response = await stub.checkboard(pokemon_game_pb2.name(hostname = hname),wait_for_ready=True)
            if(response.alive !=-1):
                if(response.lock == hname):
                    if(response.alive == -1):
                        flag = 0
                        new_x, new_y = -1, -1
                    else:
                        flag = response.pokemon_left
                        new_x, new_y = pokemon_pos_move(hname, response.pos_array, response.cur_pos)
                        response1 = await stub.Move(pokemon_game_pb2.movepos(row = new_x, column = new_y, hostname = hname), wait_for_ready=True)
                        #time.sleep(1)
                        print("I made a move")
                else:
                    pass
                    #print("Data locked")
            elif(response.alive == -1):
                #response2 = stub.trainer_list(pokemon_game_pb2.name(hostname = hname), wait_for_ready=True)
                #print("Caught by:", response.trainer)
                flag = 0
                #pass

async def trainer():
    async with grpc.aio.insecure_channel("server:50051") as channel:
        stub = pokemon_game_pb2_grpc.PokemonGameStub(channel)
        flag = 1
        hname = socket.gethostname()
        my_pokemon_list = []
        while (flag!=0):
            response = await stub.checkboard(pokemon_game_pb2.name(hostname = hname),wait_for_ready=True)
            flag = response.pokemon_left
            if(response.alive!=-1):
                if(response.lock == hname):
                    if(response.alive == -1 or response.pokemon_left == 0):
                        flag = 0
                        new_x, new_y = -1, -1
                    else:
                        flag = response.pokemon_left
                        new_x, new_y, capture_init = trainer_pos_move(hname, response.pos_array, response.cur_pos)
                        response1 = await stub.Move(pokemon_game_pb2.movepos(row = new_x, column = new_y, hostname = hname, capture = capture_init), wait_for_ready=True)
                        #time.sleep(1)
                        print("I made a move")
                else:
                    pass
                #print("Data locked")
                #pass
            elif(response.alive == -1):
                #response2 = stub.pokemon_list(pokemon_game_pb2.name(hostname = hname), wait_for_ready=True)
                #val = ''
                #for x in response2.pokemon_name:
                #    val = val + str(x) + " "
                #print("Pokemon Caught:", val)
                flag = 0

async def serve():
    server = grpc.aio.server(concurrent.futures.ThreadPoolExecutor(max_workers=20))
    pokemon_game_pb2_grpc.add_PokemonGameServicer_to_server(PokemonGame(),server)
    server.add_insecure_port('server:50051')
    #server.start()
    with open('config.json') as json_file:
        data = json.load(json_file)
    global n , no_of_pokemon, N, lock_flag, pokedex, path
    n = data['N']
    T = data['T']
    P = data['P']
    no_of_pokemon = P
    json_file.close()
    
    #define file lock
    lock_flag = 'server'
    #create board
    N = {}
    pokedex = {}
    path = {}
    
    #initiailze pokedex and path 
    for i in range(T):
        nam = 'trainer' + str(i+1)
        pokedex[nam] = []
        path[nam] = []
    for i in range(P):
        nam = 'pokemon' + str(i+1)
        path[nam] = []

    #Initalized N/board dictionary
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
            way = path[upd]
            way.append([i,j])
            path[upd] = way
            idx = idx +1

    #populate pokemon
    idx1 = 0
    while idx1 != P:
        i = rng.integers(low=0, high=n-1, size=1)[0]
        j = rng.integers(low=0, high=n-1, size=1)[0]
        #if N[i][j]==0:
        if len(N[i,j]['trainer'])==0:
            upd = 'pokemon' + str(idx1+1)
            if len(list(N[i, j]['pokemon']))>0:
                new_list = list(N[i, j]['pokemon'])
                new_list.append('pokemon'+ str(idx1+1))
            else:
                new_list = ["pokemon" + str(idx1+1)]
            N[i, j]['pokemon'] = new_list
            way = path[upd]
            way.append([i,j])
            path[upd] = way
            idx1 = idx1 +1
    
    with open('pokedex.pickle', 'wb') as handle1:
        pickle.dump(pokedex, handle1, protocol = pickle.HIGHEST_PROTOCOL)

    with open('path.pickle','wb') as handle2:
        pickle.dump(path, handle2, protocol = pickle.HIGHEST_PROTOCOL)

    with open('board.pickle', 'wb') as handle:
        pickle.dump(N, handle, protocol=pickle.HIGHEST_PROTOCOL)
    display_board(n)

    await server.start()
     # Try case to exit server
    await server.wait_for_termination()
    #try :
    #    while True:
    #        time.sleep(10)
    #except KeyboardInterrupt:
    #    server.stop(0)

def display_board(n):
    global N
    with open('node-list.json') as json_file:
        data = json.load(json_file)

    with open('board.pickle', 'rb') as handle:
        board = pickle.load(handle)

    for i2 in range(n):
        row = "|"
        for j2 in range(n):
            if len(board[i2,j2]['trainer']) > 0:
                row = row + data[board[i2,j2]['trainer']] + "|"
            elif len(board[i2,j2]['pokemon']) > 0:
                #for val in list(board[i2,j2]['pokemon']):
                val = list(board[i2,j2]['pokemon'])[0]    
                row = row + data[val] + "|"
            else:
                row = row + "__|"
        print(row)


if __name__ == '__main__':
    hostname = socket.gethostname()
    if socket.gethostname() == 'server':
        asyncio.run(serve())
    else:
        hostname = hostname[:-1]
        if hostname == "trainer":
            time.sleep(1)
            asyncio.run(trainer())
        elif hostname == "pokemon":
            time.sleep(1)
            asyncio.run(pokemon())

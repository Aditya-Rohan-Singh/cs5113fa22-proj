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
global N, n, no_of_pokemon, lock_flag, pokedex, path, board

def get_position(hostname1):
    #with FileLock("board.pickle"):
    #    with open('board.pickle', 'rb') as handle:
    #        board = pickle.load(handle)
    global board
    if(hostname1.startswith('trainer')):
        for i,k in enumerate(board):
            if(list(board.values())[i]['trainer'] == hostname1):
                x,y = k
                hostname_caught = 0
                break;

    elif(hostname1.startswith('pokemon')):
        for idx,k in enumerate(board):
            if (hostname1 in list(board.values())[idx]['pokemon']):
                x,y = k
                hostname_caught = 0
                break;
            else:
                x,y =-1,-1
                hostname_caught = -1
    return(x,y,hostname_caught)

def pokemon_left():
    global board
    i = 0
    for k,v in board.items():
        for val in list(board[k]['pokemon']):
                i = i+1
    return(i)

def possible_moves(i,j,hostname1):
    list_array = [[i-1,j-1], [i-1,j], [i-1,j+1], [i,j+1], [i+1,j+1], [i+1,j], [i+1,j-1], [i,j-1]]
    #with open('board.pickle', 'rb') as handle:
    #    board = pickle.load(handle)
    global board

    if(hostname1.startswith('pokemon')):
        pokemon_moves = [-1 if(k1 < 0 or k1 == n or k2 < 0 or k2 ==n)  else 2 if board[k1,k2]['trainer'].startswith('trainer') else 0 if(len(board[k1,k2]['pokemon']) > 1) else 0 for (k1,k2) in list_array ]
    elif(hostname1.startswith('trainer')):
        pokemon_moves = [-1 if(k1 < 0 or k1 == n or k2 < 0 or k2 ==n)  else -1 if board[k1,k2]['trainer'].startswith('trainer') else 1 if(len(board[k1,k2]['pokemon']) > 0) else 0 for (k1,k2) in list_array ]

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
                val = pokemon_left()
                if(val==0):
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
        global lock_flag, board
        if(lock_flag==request.hostname):
            #with open('board.pickle', 'rb') as handle:
            #    board = pickle.load(handle)
            with open('pokedex.pickle','rb') as handle:
                poked = pickle.load(handle)
            with open('catch.pickle','rb') as handle:
                catch = pickle.load(handle)

            #update move
            if(request.hostname.startswith('trainer')):
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
                            for val in list(board[(request.row,request.column)]['pokemon']):
                                catch[val] = [request.row,request.column]
                                print(catch[val])
                        else:
                            val = board[(request.row, request.column)]['pokemon'][0]
                            print(val)
                            catch[val] = [request.row,request.column]
                            print(catch)
                            poked[request.hostname] = board[(request.row,request.column)]['pokemon']
                            no_of_pokemon = no_of_pokemon - 1
                        
                        board[(request.row,request.column)]['pokemon'] = []
            elif(request.hostname.startswith('pokemon')):
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

            #print(catch)
            #Update caught
            with open('catch.pickle','wb') as handle:
                pickle.dump(catch, handle, protocol=pickle.HIGHEST_PROTOCOL)


            #update path 
            with open('path.pickle', 'rb') as handle:
                path = pickle.load(handle)
            if((old_i, old_j) != (request.row, request.column)):
                row = path[request.hostname]
                row.append([request.row, request.column])
                path[request.hostname] = row
            print(poked, no_of_pokemon)

            with open('path.pickle', 'wb') as handle:
                pickle.dump(path, handle, protocol=pickle.HIGHEST_PROTOCOL)

            with open('pokedex.pickle','wb') as handle1:
                pickle.dump(poked, handle1,  protocol=pickle.HIGHEST_PROTOCOL)

            
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
    
    def trainer_list(self, request,context):
        with open('pokedex.pickle', 'rb') as handle:
            poked = pickle.load(handle)

        for k,v in poked.items():
            if request.hostname in list(v):
                trainer_name = k
        return(pokemon_game_pb2.trainer_name(trainer = trainer_name))

    def client_path(self, request, context):
        with open('path.pickle','rb') as handle:
            pat = pickle.load(handle)
        
        pat1 = pat[request.hostname]
        new_pat = [item for p in pat1 for item in p]
        return(pokemon_game_pb2.path(path_followed = new_pat))

    def caught_location(self, request, context):
        with open('catch.pickle','rb') as handle:
            catch = pickle.load(handle)
        print(catch)
        (x1,y1) = catch[request.hostname]
        return(pokemon_game_pb2.pos(r = x1, c = y1))

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
                        time.sleep(1)
                        print("I made a move")
                else:
                    pass
                    #print("Data locked")
            elif(response.alive == -1):
                response2 = await stub.trainer_list(pokemon_game_pb2.name(hostname = hname), wait_for_ready=True)
                print("Caught by:", response2.trainer)
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
                        time.sleep(1)
                        print("I made a move")
                else:
                    pass
            elif(response.alive == -1):
                response2 = await stub.pokemon_list(pokemon_game_pb2.name(hostname = hname), wait_for_ready=True)
                val = ''
                for x in response2.pokemon_name:
                    val = val + str(x) + " "
                    response4 = await stub.client_path(pokemon_game_pb2.name(hostname = x), wait_for_ready = True)
                    path_val = response4.path_followed
                    new_path_val = [[path_val[i],path_val[i+1]] for i in range(0,len(path_val),2)]
                    response5 = await stub.caught_location(pokemon_game_pb2.name(hostname = x), wait_for_ready = True)
                    
                    print(f"Path Followed by pokemon {x}:{new_path_val}")
                    print(f"{x} caught at ({response5.r},{response5.c})")
                print("Pokemon Caught:", val)
                response3 = await stub.client_path(pokemon_game_pb2.name(hostname = hname), wait_for_ready = True)
                path_val = response3.path_followed
                new_path_val = [[path_val[i],path_val[i+1]] for i in range(0,len(path_val),2)]
                print("Path Followed:", new_path_val)
                flag = 0

async def serve():
    server = grpc.aio.server(concurrent.futures.ThreadPoolExecutor(max_workers=50))
    pokemon_game_pb2_grpc.add_PokemonGameServicer_to_server(PokemonGame(),server)
    server.add_insecure_port('server:50051')
    with open('config.json') as json_file:
        data = json.load(json_file)
    global n , no_of_pokemon, N, lock_flag, pokedex, path, board
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
    catch_details = {}
    #initiailze pokedex and path 
    for i in range(T):
        nam = 'trainer' + str(i+1)
        pokedex[nam] = []
        path[nam] = []
    for i in range(P):
        nam = 'pokemon' + str(i+1)
        path[nam] = []
        catch_details[nam] = []

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

    with open('catch.pickle', 'wb') as handle:
        pickle.dump(catch_details, handle, protocol = pickle.HIGHEST_PROTOCOL)

    #with open('board.pickle', 'wb') as handle:
    #    pickle.dump(N, handle, protocol=pickle.HIGHEST_PROTOCOL)
    board = N
    display_board(n)

    await server.start()
     # Try case to exit server
    await server.wait_for_termination()
    #try :
    #    while True:
    #        time.sleep(10)
    #except KeyboardInterrupt:
    #    server.stop(0)
    display_board(n)

def display_board(n):
    global N
    with open('node-list.json') as json_file:
        data = json.load(json_file)

    #with open('board.pickle', 'rb') as handle:
    #    board = pickle.load(handle)
    
    global board
    
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
        #hostname = hostname[:-1]
        if hostname.startswith("trainer"):
            asyncio.run(trainer())
        elif hostname.startswith("pokemon"):
            asyncio.run(pokemon())

#!/usr/bin/env python3
import argparse


trainer_list = ["\U0001F480", "\U0001F9D2", "\U0001F466", "\U0001F467", "\U0001F9B3", "\U0001F468", "\U0001F469", "\U0001F64D", "\U0001F475", "\U0001F9D3"]
pokemon_list = ["\U0001F412", "\U0001F98D", "\U0001F43A", "\U0001F98A", "\U0001F436", "\U0001F431", "\U0001F981", "\U0001F42E", "\U0001F437", "\U0001F42D"]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, choices = range(1,10), required=True)
    parser.add_argument('--T', type=int, choices = range(1,10), required=True)
    parser.add_argument('--P', type=int, choices = range(1,10), required=True)

    args = parser.parse_args()
    f = open("docker-compose.yml","w")
    f.write("version: '3.7'\n\n")
    f.write("services:\n  server:\n    build: .\n    hostname: server\n    container_name: Server\n    networks:\n      - default")
    for idx in range(args.T):
        row = "\n  client"+str(idx+1)+":\n    build: .\n    hostname: " + trainer_list[idx] + "\n    container_name: " + trainer_list[idx] + "\n    networks:\n      - default"
        f.write(row)

    for idx1 in range(args.P):
        row =  "\n  client"+str(args.T+idx1+1)+":\n    build: .\n    hostname: " + pokemon_list[idx1] + "\n    container_name: " + pokemon_list[idx1] + "\n    networks:\n      - default"
        f.write(row)

    f.close()
        
        


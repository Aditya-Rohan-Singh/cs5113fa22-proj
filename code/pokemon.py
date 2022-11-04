#!/usr/bin/env python3
import argparse


trainer_list = ["\U0001F9D2", "\U0001F9D2", "\U0001F466", "\U0001F467", "\U0001F9B3", "\U0001F468", "\U0001F469", "\U0001F64D", "\U0001F475", "\U0001F9D3"]
pokemon_list = []


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
        row = "  client"+str(idx+1)+":\n    build: .\n    hostname: " + trainer_list[idx] + "\n    container_name: " + trainer_list[idx] + "\n    networks:\n      - default"
        f.write(row)

    f.close()
        
        


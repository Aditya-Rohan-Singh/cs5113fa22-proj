#!/usr/bin/env python3
import argparse
import json

trainer_list = ["\U0001F480", "\U0001F9D2", "\U0001F466", "\U0001F467", "\U0001F9B3", "\U0001F468", "\U0001F469", "\U0001F64D", "\U0001F475", "\U0001F9D3", "\U0001F600", "\U0001F643", "\U0001F602", "\U0001F60D","\U0001F911", "\U0001F915", "\U0001F922", "\U0001F975", "\U0001F976", "\U0001F60E", "\U0001F637", "\U0001F644", "\U0001F61F","\U0001F629", "\U0001F47F", "\U0001F608", "\U0001F621", "\U0001F47D", "\U0001F47B", "\U0001F916"]
pokemon_list = ["\U0001F412", "\U0001F98D", "\U0001F43A", "\U0001F98A", "\U0001F436", "\U0001F431", "\U0001F981", "\U0001F42E", "\U0001F437", "\U0001F42D", "\U0001F648", "\U0001F649", "\U0001F64A","\U0001F99D", "\U0001F42F", "\U0001F434", "\U0001F984", "\U0001F993", "\U0001F417", "\U0001F418", "\U0001F42A", "\U0001F42D", "\U0001F999", "\U0001F992", "\U0001F98F", "\U0001F439", "\U0001F439", "\U0001F430", "\U0001F987", "\U0001F43B"]

for t in trainer_list:
    print(t)

for p in pokemon_list:
    print(p)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, choices = range(1,21), required=True)
    parser.add_argument('--T', type=int, choices = range(1,30), required=True)
    parser.add_argument('--P', type=int, choices = range(1,30), required=True)

    args = parser.parse_args()
    f = open("docker-compose.yml","w")
    f1 = open("node-list.json","w")
    f2 = open("config.json","w")
    dict = {'N':args.N, "T":args.T, "P": args.P}
    json_file = json.dumps(dict)
    f2.write(json_file)
    f2.close()

    ## Starting docker-compose.yml write
    f.write("version: '3.7'\n\n")
    f.write("services:\n  server:\n    build: .\n    hostname: server\n    container_name: Server\n    networks:\n      - default")
    
    dict ={}
    for idx in range(args.T):
        row = "\n  client"+str(idx+1)+":\n    build: .\n    hostname: trainer" + str(idx+1) +"\n    container_name: trainer" + str(idx+1) + "\n    networks:\n      - default"
        f.write(row)
        dict["trainer"+str(idx+1)] = str(trainer_list[idx])
        #f1.write("Trainer" + str(idx+1) + ": " + trainer_list[idx]+ "\n")

    for idx1 in range(args.P):
        row =  "\n  client"+str(args.T+idx1+1)+":\n    build: .\n    hostname: pokemon" + str(idx1+1) + "\n    container_name: pokemon" + str(idx1+1) + "\n    networks:\n      - default"
        f.write(row)
        #f1.write("Pokemon" + str(idx1+1) + ": " + pokemon_list[idx1]+ "\n")
        dict["pokemon"+str(idx1+1)] = str(pokemon_list[idx1])

    json1 = json.dumps(dict)
    f1.write(json1)
    f.close()
    f1.close()
        
        


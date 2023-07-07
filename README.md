# cs5113fa22-proj - THe Pokemon Game
Final Project for cs5113- Distributed Systems.



## Development Schedule

|Date|Description|Progress|
|-----|-----|------|
|11/01/22|Create dynamic docker-compose.yml file based on user input|Complete|
|11/03/22|Protos and Interface Design|Complete|
|11/17/22|First Version Logging|Complete|
|11/20/22|Trainer and Pokemon move across board|Complete|
|11/25/22|Trainer Capturing pokemon|Complete|
|12/14/22|Project Submission|Not Started|


## Execution steps

- As per the submission steps, the number of Pokemon and trainers for my project will be 26(10 + 10(J) + 6(Aditya))

- ./pokemon.py --N 20 --T 26 --P 26

- docker-compose up --build

## How the board is displayed

- The function display\_board() when called will display the current board from the server. It stores the hostnames of the server in an n*n matrix and while displaying retrieves the emoji assigned to each node from a json file called node-list.json while stores a dictionary in the format hostname:emoji 

- Note: The GIF might take some to load. But it is there in the README.md

## Milestone 3 gif
![](https://github.com/Aditya-Rohan-Singh/cs5113fa22-proj/blob/main/milestone3.gif)




### Creating Trainer and Pokemon Nodes

- When you execute the script pokemon.py with command line arguments.
1. N to create the board N\*N, which will be stored in an enviroment variable used by the server container to initialize and store the board.
2. T which stores the number of trainers.
3. P which stores the number of pokemon.

- The script pokemon.py will use T and P to dynamically add the number of pokemon P and trainers T by adding the below lines of code to docker-compose.yml:
client[i]:
    build: .
    hostname: t/p<idx>
    container_name: Trainer/Pokemon<idx>
    networks:
      - default  
where i is an index tracking the number of P and T.

- The script will utilize a list of pre-saved 30 human emoji and animal emoji to assign hostname to Trainer and POkemon respectively.

- The script will also create a list of Trainers and Pokemon as per the given user input and store it with their respective emoji in a json file called node-list.json

)
- The docker file will be similar to what we used in Assignment 1 with no changes except the proto file name.

- The protocol buffer files will be created as per the requirment of the project and when the script is executed, the docker-compose command will execute and build up the protocol buffer files to create the buffer files using the .proto file.



# RPC functions 

### checkboard

- The function takes the hostname of the client requesting as input
- It checks who holds the current lock on the data. If it is server which means the lock is free, the client will change the hostname to its own so no other client can access it. Otherwise it will send back empty lists of values with the lock to the client. The client will keep on trying till it has the lock.
- Once it has the lock,
- The function based on hostname gets the current position of the client from the dictionary.
- It calculates an array of values around the client. Going from top right in a clockwise direction so the array will be of size 8. 
- The below values are the coordinates around it. The function will create another list which will just store what kind of movement that the client can do on the particular coordinates.
[[i-1,j-1], [i-1,j], [i-1,j+1], [i,j+1], [i+1,j+1], [i+1,j], [i+1,j-1], [i,j-1]]

- For trainers, -1 for out of bounds or another trainer, 1 for pokemon and 0 for empty space
- For Pokemons, -1 for out of bounds, 2 for trainers and 0 for empty spaces.

- It also checks if the server are suppossed to be alive or not and returns that. For trainers, they will be alive as long as the no\_of\_pokemons is greate than 0. For Pokemon, as long as they are not caught. Once they are caught it will change the alive value to -1.


### move

- Client will call this function and give the coordinates it want to move to as input. For Trainers, it will also send a caught value if it has pokemon on the position it is moving to.

- If the client is the one still holding the lock, it will proceed ahead with the movements.
- For trainer, It again gets the original position and updated the board that it has moved to the new position
	- If the capture value is 1, that means the trainer wants to capture the pokemon at its new position 
	- The board is updated as captured pokemons are removed, global variable tracking the no of pokemon is decreased by the number of pokemon caught.
	- Pokedex is updated.
- For pokemon,
	- No need of capture values. It moves and updated the board where it has moved.

- Path is updated for the move pokemon or trainer moved. 

- Lock is released back to teh server


### pokemon\_list

- Takes the trainer name as input and then returns the pokemon it has captured as output. The trainer then stores the information in the pokedex on the pokemon captured.

### client\_path

- Takes the hostname as input and returns the path as output which has been taken by the trainer/pokemon

### trainer\_list

- Takes the pokemon name as input and then returns the trainer that captured it. The pokemon then stores the information that who captured it.

### caught\_location

- Takes the pokemon name as input and returns the location it was captured at. The trainer is calling this function.

# Other functions used by client

### get\_position

- It gets the current position based on hostname from the board. If it is a pokemon, it also returns if you are caught or not. which is then used as the alive flag.

### possible\_moves

- The below values are the coordinates around it. The function will create another list which will just store what kind of movement that the client can do on the particular coordinates.
[[i-1,j-1], [i-1,j], [i-1,j+1], [i,j+1], [i+1,j+1], [i+1,j], [i+1,j-1], [i,j-1]]

- For trainers, -1 for out of bounds or another trainer, 1 for pokemon and 0 for empty space
- For Pokemons, -1 for out of bounds, 2 for trainers and 0 for empty spaces.

### trainer\_pos\_move

- It takes the array recieved from server of possible moves from input and the original position and decides where the trainer will move.
- Based on available moves, it will randomly choose a move. Prefernce is given to if a pokemon is at that position or the value 1.

### pokemom\_pos\_move

- It takes the array recieved from server of possible moves from input and the original position and decides where the pokemon will move. 
- Based on available moves, if there is a trainer near it the pokemon will move otherwise it will not.
- It will filter out moves which will take it closer to the trainer by calculating the distance between them. If the distance of the possible move is 1 or less, that move will be removed from possible moves.

# Distributed Problems

### Concurrency
- I implemented Pessimistic concurrency control to make sure only one client(trainer/pokemon) is making a move at a time by locking the data. The hostname of the clients are being utilized as the lock name.

- The papers discussed in class specifically , Chubby and Omega gave me the idea to implement this pessimistic concurrency control.

### Communication
- To achieve asynchronous messaging, so the clients are talking to the server in no particular order, I implemented asynchrous messaging using the Asyncio grpc API.
- References:
	- [Github for Asyn GRPC examples](https://github.com/grpc/grpc/tree/master/examples/python/helloworld)
	- [GRPC Aysnc documentation](https://grpc.github.io/grpc/python/grpc_asyncio.html)

### Consistency
- I just maintained one copy of the data that was being utilized at the server size. Clients had to request the data from server whenever they had to makek a move.

### Sclaing
- Technically, all clients should have their own cores for execution. But currently we are utilizing only 8 cores (max 24 available in the US region)

 

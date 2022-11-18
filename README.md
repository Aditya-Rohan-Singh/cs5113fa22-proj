# cs5113fa22-proj
Final Project for cs5113


## Development Schedule

|Date|Description|Progress|
|-----|-----|------|
|11/01/22|Create dynamic docker-compose.yml file based on user input|Complete|
|11/03/22|Protos and Interface Design|Complete|
|11/17/22|First Version Logging|Complete|
|11/20/22|Trainer and Pokemon move across board|In-Progress|
|11/25/22|Trainer Capturing pokemon|Not Started|
|12/01/22|Project Submission|Not Started|


## First version logging

- The function display\_board() when called will display the current board from the server. It stores the hostnames of the server in a n\*n matrix and while displaying retrieves the emoji assigned to each node from a json file called node-list.json while stores a dictionary in the format hostname:emoji 




![](https://github.com/Aditya-Rohan-Singh/cs5113fa22-proj/blob/main/milestone3.gif)


## Emoji Chooser

### Creating Trainer and Pokemon Nodes

- When you execute the script pokemon.py with command line arguments.
1. N to create the board N\*N, which will be stored in an enviroment variable used by the server container to initialize and store the board.
2. T which stores the number of trainers.
3. P which stores the number of pokemon.

- The script pokemon.py will use T and P to dynamically add the number of pokemon P and trainers T by adding the below lines of code to docker-compose.yml:
client[i]:
    build: .
    hostname: <emoji>
    container_name: <emoji>
    networks:
      - default  
where i is an index tracking the number of P and T.

- The script will utilize a list of pre-saved 25 human emoji and animal emoji to assign hostname to Trainer and POkemon respectively.

- The script will also create a list of Trainers and Pokemon as per the given user input and store it with their respective emoji in a json file called node-list.json

- Once the docker-compose.yml file is dynamically created, the script will utilize the subprocess package to execute the command "docker-compose up --build: which will create the mentioned containers in the docker-compose.yml file that was dynamically created based on user input.

- The docker file will be similar to what we used in Assignment 1 with no changes.

- The protocol buffer files will be created as per the requirment of the project and when the script is executed, the docker-compose command will execute and build up the protocol buffer files to create the buffer files using the .proto file.



# Interface 

### checkboard

- The function takes the hostname of the client requesting as input and sends an array of values around it as output. Going from top right in a clockwise direction so the array will be of size 8. 

- -1 will stand for cannot move either due to no places to move or an existing trainer. 1 for a possible move and 2 for a possible move with pokemon available for capture on the position.

### move

- You send the message movepos which has the row number, column number and hostname as data. The row and column data will be used to move the Trainer or pokemon and the hostname will be used to log their movements. The output will be a flag which says the move has been completed or not.

- There will be seperate cases in case of pokemon and trainers, as pokemon can move into same position as other pokemon but trainers cannot.
### pokemon\_list

- Takes the trainer name as input and then returns the pokemon it has captured as output. The trainer then stores the information in the pokedex on the pokemon captured.

### client\_path

- Takes the hostname as input and returns the path as output which has been taken by the trainer/pokemon

### trainer\_list

- Takes the pokemon name as input and then returns the trainer that captured it. The pokemon then stores the information that who captured it.

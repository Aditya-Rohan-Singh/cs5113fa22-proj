# cs5113fa22-proj
Final Project for cs5113


## Development Schedule

|Date|Description|Progress|
|-----|-----|------|
|11/01/22|Create dynamic docker-compose.yml file based on user input|In-Progress|
|11/03/22|Protos and Interface Design|In-Progress|
|11/15/22|Trainer and Pokemon move across board|Not Started|
|11/17/22|First Version Logging|Not Started|
|11/25/22|Trainer Capturing pokemon|Not Started|
|12/01/22|Project Submission|Not Started|


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

- The script will also create a list of Trainers and Pokemon as per the given user input. 

- Once the docker-compose.yml file is dynamically created, the script will utilize the subprocess package to execute the command "docker-compose up --build: which will create the mentioned containers in the docker-compose.yml file that was dynamically created based on user input.

- The docker file will be similar to what we used in Assignment 1 with no changes.

- The protocol buffer files will be created as per the requirment of the project and when the script is executed, the docker-compose command will execute and build up the protocol buffer files to create the buffer files using the .proto file.

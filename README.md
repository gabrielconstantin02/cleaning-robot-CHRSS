# Project Software Engineering course
cleaning-robot-CHRSS -> vacuuming & mopping smart robot  

## How to run the project  

### Prerequirements:  

1. Create an virtual environment and install the requirements.txt
2. Install [mosquitto](https://mosquitto.org/)

### Running the project:

0. enable virtual environment:  
    ```console
    foo@project:~$ source path-to-venv/bin/activate
    ```

1. run mosquitto:  
    ```console
    foo@project:~$ mosquitto
    ```
2. export flask env and flask run  
    ```console
    foo@project:~$ export FLASK_ENV=development
    foo@project:~$ export FLASK_APP=cleaning-robot/app.py
    ```
3. initialize database:  
    ```console
    foo@project:~$ flask init-db
    ```
4. run the project:  
    ```console
    foo@project:~$ python cleaning-robot/app.py
    ```
   
### Testing:  

#### HTTP:  

To test the http connection and api you can use something like [postman](https://www.postman.com/)

#### MQTT:  

To test the MQTT we need to first make a GET request to localhost:5000/start_MQTT which will start the mqtt thread  
Next we need to use mosquitto_sub to connect to the mosquitto broker on the topic robot/status:  
   ```console
   foo@project:~$ mosquitto_sub -v -t "robot/status"
   ```

## CHRSS Team members:
- **[Constantin Gabriel-Adrian](https://github.com/Kira060200)**
- **[Hernest Mihai](https://github.com/mihaihe1)**
- **[Richițeanu Mihai-Sebastian](https://github.com/SebastianRichiteanu)**
- **[Sociu Daniel](https://github.com/danielsociu)**
- **[Stoicesu Adrian-Nicolae](https://github.com/Deadlykittenn)**

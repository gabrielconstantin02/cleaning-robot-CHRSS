# CHRSS - cleaning-robot

## About

This is a backend app for a cleaning robot.
The app was created to improve your life style and save you time.

### Built with

<li><a href="https://www.python.org/"> Python </a></li>
<li><a href="https://flask.palletsprojects.com/en/2.0.x/"> Flask </a></li>
<li> <a href="https://docs.python-requests.org/en/latest/"> Requests</a></li>
<li><a href="https://docs.pytest.org/en/6.2.x/"> Pytest </a> (for automation testing)</li>
<li><a href="https://openweathermap.org/api">Open Weather App</a> (for air pollution stats)</li>
<li> <a href="https://coverage.readthedocs.io/en/6.3/"> Coverage</a> (for automation testing coverage)</li>

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

## Automation tests

#### Unit tests:

To run the unit tests open a terminal, cd into the project folder and run: ```python3 -m pytest cleaning-robot/unit_test/*```

#### Integration tests:

To run the integration tests open a terminal, cd into the project folder and run: ```python3 -m pytest cleaning-robot/intergation_test/*```

#### Tests coverage
To see tests coverage, use
```python3 -m coverage run -m pytest cleaning-robot/unit_test/*``` or ```python3 -m coverage run -m pytest cleaning-robot/unit_test/*``` and to see the report use
```python3 -m coverage report```



## Backlog

See the [open issues](https://github.com/Kira060200/cleaning-robot-CHRSS/projects/1) for the full list of features.

## CHRSS Team members:
- **[Constantin Gabriel-Adrian](https://github.com/Kira060200)**
- **[Hernest Mihai](https://github.com/mihaihe1)**
- **[Richițeanu Mihai-Sebastian](https://github.com/SebastianRichiteanu)**
- **[Sociu Daniel](https://github.com/danielsociu)**
- **[Stoicesu Adrian-Nicolae](https://github.com/Deadlykittenn)**


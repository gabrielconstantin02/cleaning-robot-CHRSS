# Project Software Engineering course
cleaning-robot-CHRSS -> vacuuming & mopping smart robot  

## How to run the project  

### Prerequirements:  

1. Create an environment and install the requirements.txt
2. Install mosquitto 

### Running the project:

1. run mosquitto: 
    '''console
    foo@bar:~$ mosquitto
    '''
2. export flask env and flask run
    '''console
    export FLASK_ENV=development
    export FLASK_APP=cleaning-robot/app.py
    '''
3. initialize database:
    '''console
    flask init-db
    '''
4. run the project:
    '''console
    python cleaning-robot/app.py
    '''

## CHRSS Team members:
- **[Constantin Gabriel-Adrian](https://github.com/Kira060200)**
- **[Hernest Mihai](https://github.com/mihaihe1)**
- **[Richițeanu Mihai-Sebastian](https://github.com/SebastianRichiteanu)**
- **[Sociu Daniel](https://github.com/danielsociu)**
- **[Stoicesu Adrian-Nicolae](https://github.com/Deadlykittenn)**

import os
from flask import Flask
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from threading import Thread
import json
import time
import eventlet

import db
import auth
import environment
import cleaning
import vacuum_settings
import mop_settings
import cleaning_schedule
import status
import air_quality
import automatic_empty

app = None
mqtt = None
socketio = None
thread = None

eventlet.monkey_patch()

def create_app(test_config=None):

    # create and configure the app
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cleaning-robot.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

   # a simple page that says hello
    @app.route('/hello')
    def hello():
        global thread
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()
        return 'Hello, World!'

    app.register_blueprint(auth.bp)
    app.register_blueprint(environment.bp)
    app.register_blueprint(cleaning.bp)
    app.register_blueprint(vacuum_settings.bp)
    app.register_blueprint(mop_settings.bp)
    app.register_blueprint(cleaning_schedule.bp)
    app.register_blueprint(air_quality.bp)
    app.register_blueprint(automatic_empty.bp)

    return app

def create_mqtt_app():
    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt
    mqtt = Mqtt(app)
    global socketio
    socketio = SocketIO(app, async_mode="eventlet")

    return mqtt


# Start MQTT publishing

# Function that every second publishes a message
def background_thread():
    count = 0
    while True:
        time.sleep(1)
        # Using app context is required because the get_status() functions
        # requires access to the db.
        with app.app_context():
            message = json.dumps(status.get_status(), default=str)
        # Publish
        mqtt.publish('python/mqtt', message)


# App will now have to be run with `python app.py` as flask is now wrapped in socketio.
# The following makes sure that socketio is also used

def run_socketio_app():
    create_app()
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)

    @socketio.on('publish')
    def handle_publish(json_str):
        data = json.loads(json_str)
        mqtt.publish(data['topic'], data['message'])


    @socketio.on('subscribe')
    def handle_subscribe(json_str):
        data = json.loads(json_str)
        mqtt.subscribe(data['topic'])


    @socketio.on('unsubscribe_all')
    def handle_unsubscribe_all():
        mqtt.unsubscribe_all()


    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        data = dict(
            topic=message.topic,
            payload=message.payload.decode()
        )
        socketio.emit('mqtt_message', data=data)


    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)



if __name__ == '__main__':
    run_socketio_app()


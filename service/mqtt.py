import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import os
from dotenv import load_dotenv
from paho import mqtt

load_dotenv()

hostname = os.getenv("MQTT_URL")
print(os.getenv("MQTT_PORT"))
port = int(os.getenv("MQTT_PORT"))


class MQTTService:
    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("connect received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def single_publish(self, client, userdata, mid, properties=None):
        client.loop_stop()

    # print which topic was subscribed to
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # print message, useful for checking if it was successful
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def _init(self) -> paho.Client:
        try:
            # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
            # userdata is user defined data of any type, updated by user_data_set()
            # client_id is the given name of the client
            client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
            client.on_connect = self.on_connect

            # enable TLS for secure connection
            client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
            # set username and password
            client.username_pw_set("smaglator", "smaglatorkey")
            return client
        except Exception as e:
            raise e("unable connect create mqtt client")

    def start_connection(self) -> paho.Client:
        try:
            client = self._init()
            # connect to HiveMQ Cloud on port 8883 (default for MQTT)
            client.connect(hostname, port)

            # setting callbacks, use separate functions like above for better visibility
            client.on_subscribe = self.on_subscribe
            client.on_message = self.on_message
            client.on_publish = self.on_publish
            return client
        except Exception as e:
            raise e

    def send_message(self, client: paho.Client, message: str, topic: str, qos: int = 1):
        client.publish(topic=topic, payload=message, qos=qos)

    def disconnect_after_publish(self, client: paho.Client):
        client.loop_stop()
        client.disconnect()

    def listned_message(self, client: paho.Client, topic: str, qos: int = 1):
        client.on_message

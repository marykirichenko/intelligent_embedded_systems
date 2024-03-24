from paho.mqtt import client as mqtt_client
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from schema.aggregate_parking_schema import AggregatedParkingDataSchema
from file_datasource import FileDatasource
import config

import logging

def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, parking_topic, basic_topic, datasource, delay):
    datasource.startReading()
    logging.basicConfig(filename='formedDataParking.log', level=logging.INFO)
    while True:
        time.sleep(delay)
        data = datasource.read("basic")
        if data is not None:
            msg = AggregatedDataSchema().dumps(data)
            result = client.publish(basic_topic, msg)
            status = result[0]
            if status == 0:
                pass
                # print(f"Send `{msg}` to topic `{basic_topic}`")
            else:
                print(f"Failed to send message to topic {basic_topic}")

        time.sleep(delay)
        data = datasource.read("parking")
        if data is not None:
            logging.info(data)
            msg = AggregatedParkingDataSchema().dumps(data)
            result = client.publish(parking_topic, msg)  # Publish to the parking topic
            status = result[0]
            if status == 0:
                pass
                # print(f"Send `{msg}` to topic `{parking_topic}`")
            else:
                print(f"Failed to send message to topic {parking_topic}")



def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    # Infinity publish data
    publish(client, config.PARKING_TOPIC, config.BASIC_TOPIC, datasource, config.DELAY)



if __name__ == "__main__":
    run()

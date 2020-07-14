# -*- coding: utf-8 -*-
from lib.AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from lib import logging

QOS_AT_LEAST_ONCE = 1


class AwsIotController:

    def __init__(self, aws_iot_endpoint, client_certificate, private_key, root_ca, client_id,
                 conn_disconnect_timeout, mqtt_oper_timeout):
        self.logger = logging.get_logger(__name__)
        self.endpoint = aws_iot_endpoint
        self.client_certificate = client_certificate
        self.private_key = private_key
        self.root_ca = root_ca
        self.client_id = client_id
        self.conn_disconnect_timeout = conn_disconnect_timeout
        self.mqtt_oper_timeout = mqtt_oper_timeout

    def initialize(self):
        """
            Initialize the connection to the MQTT IoT Core broker
        """
        self.logger.info("Initializing connection to the MQTT broker.")
        self.client = AWSIoTMQTTClient(self.client_id)
        self.client.configureEndpoint(self.endpoint, portNumber=8883)
        self.client.configureCredentials(CAFilePath=self.root_ca, KeyPath=self.private_key,
                                         CertificatePath=self.client_certificate)
        self.client.configureConnectDisconnectTimeout(self.conn_disconnect_timeout)
        self.client.configureMQTTOperationTimeout(self.mqtt_oper_timeout)
        if self.client.connect():
            self.logger.info("Connected!")

    def subscribe(self, topic):
        """
            Subscribe to a topic

        :param topic: Topic name
        """
        topic = "{0}/{1}".format(self.client_id, topic)
        self.logger.info("Subscribing to topic '{}'...".format(topic))
        self.client.subscribe(
            topic=topic,
            QoS=QOS_AT_LEAST_ONCE,
            callback=self._on_message_received)
        self.logger.info("Subscribed to topic {}".format(topic))

    def publish(self, message, topic):
        """
            Publish a message to a topic

        :param message: String Message (example: 'hello world!')
        :param topic: String Topic name (example: test)
        """
        topic = "{0}/{1}".format(self.client_id, topic)
        self.logger.info("Publishing message to topic '{}': {}".format(topic, message))
        self.client.publish(
            topic=topic,
            payload=message,
            QoS=QOS_AT_LEAST_ONCE)

    def disconnect(self):
        """
            Disconnect the MQTT connection
        """
        self.client.disconnect()
        self.logger.warning("Disconnected!")

    def _on_message_received(self, client, userdata, message):
        """
            Handle on message received event

        :param client: Client information
        :param userdata: Userdata
        :param message: Message payload
        """
        self.logger.info("Received message from topic '{}': {}".format(message.topic, message.payload))

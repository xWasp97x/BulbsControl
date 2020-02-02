from logger import MyLogger
from umqtt_simple2 import MQTTClient
import json
from configuration_loader import ConfigurationLoader


class Updater:
	def __init__(self, config_file):
		self.config_loader = ConfigurationLoader(config_file)
		configs = self.config_loader.load_configuration('check_delay', 'broker', 'topic', 'mqtt_id', 'installed_version_file', 'mqtt_logger_conf')
		self.check_delay = int(configs['check_delay'])
		self.logger = MyLogger(True, configs['mqtt_logger_conf'])
		self.mqtt_client = MQTTClient(configs['mqtt_id'], configs['broker'])
		self.mqtt_client.DEBUG = True
		self.mqtt_client.set_callback(self.read_update)
		self.mqtt_topic = configs['topic']

	def read_update(self, topic, msg, retained, duplicate):
		print(json.loads(msg))
		self.reset_retained()

	def reset_retained(self):
		try:
			self.mqtt_client.publish(self.mqtt_topic, '', retain=True)
		except:
			None

	def fetch_update(self):
		mqtt_client = self.mqtt_client
		if not self._connected_to_mqtt():
			self.logger.log('WARNING', 'Updater', 'Reconnecting to the broker')
			try:
				mqtt_client.connect()
				self.mqtt_client.subscribe(self.mqtt_topic)
				self.logger.log('DEBUG', 'Updater', 'Reconnected to the broker')
			except:
				self.logger.log('ERROR', 'Updater', 'Broker reconnection error!')

		try:
			mqtt_client.check_msg()
		except:
			None

	def _connected_to_mqtt(self):
		try:
			self.mqtt_client.ping()
			return True
		except:
			return False







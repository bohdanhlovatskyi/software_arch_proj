# from configparser import ConfigParser
# from confluent_kafka import Producer, Consumer

# config_parser = ConfigParser(interpolation=None)
# with open('config.properties', 'r') as config_file:
#     config_parser.read_file(config_file)
# client_config = dict(config_parser['kafka_client'])

# image_producer = Producer(client_config)
# query_result_consumer = Consumer(client_config)

import os, sys, json, datetime
from bson.objectid import ObjectId
import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
        	return o.strftime(TIMESTAMP_PATTERN)
        elif isinstance(o, bytes):
        	return '0x' + o.hex()
        return json.JSONEncoder.default(self, o)
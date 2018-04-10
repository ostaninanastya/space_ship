import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

from converters import time_to_str, date_to_str

from person_mapper import PersonMapper

class ControlActionMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()
    
    macaddress = graphene.String()
    userid = graphene.String()
    user = graphene.Field(PersonMapper)

    command = graphene.String()
    params = graphene.String()
    result = graphene.String()

    def resolve_user(self, info):
    	return PersonMapper(id = self.userid)

    @staticmethod
    def init_scalar(item):
        return ControlActionMapper(date = date_to_str(item.date), 
                                   time = time_to_str(item.time),
                                   macaddress = item.mac_address.hex(),\
                                   #username = mongo_adapter.get_name_by_id('user_test', item.user_id.hex()),
                                   command = item.command,
                                   params = item.params,
                                   result = item.result,
                                   userid = item.user_id.hex())

    @staticmethod
    def init_scalar_dict(item):
        return ControlActionMapper(date = date_to_str(item['date']), 
                                   time = time_to_str(item['time']),
                                   macaddress = item['mac_address'].hex(),\
                                   #username = mongo_adapter.get_name_by_id('user_test', item.user_id.hex()),
                                   command = item['command'],
                                   params = item['params'],
                                   result = item['result'],
                                   userid = item['user_id'].hex())
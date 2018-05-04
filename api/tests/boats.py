import unittest
from urllib.request import urlopen
import json

MIN = 3

class TestBoatsCrud(unittest.TestCase):

    def switch_existential_state(self, operation, fields, where):
        result = urlopen('http://localhost:1881/api/{0}/boat/fields={1}&where={2}'.format(operation, ','.join(fields), 
            ','.join([str(key) + ':' + str(where[key]) for key in where])))
        return json.loads(result.read())['{0}Boat'.format(operation)]['boat']

    def create(self, fields, where):
        return self.switch_existential_state('create', fields, where)

    def remove(self, fields, where):
        return self.switch_existential_state('remove', fields, where)

    def update(self, fields, where, set_fields):

        collection = 'boats'
        
        result = urlopen('http://localhost:1881/api/{0}/fields={1}&where={2}&set={3}'.format(collection, ','.join(fields), 
            ','.join([str(key) + ':' + str(where[key]) for key in where]),
            ','.join([str(key) + ':' + str(set_fields[key]) for key in set_fields])))

        return json.loads(result.read())['updateBoats']['boats']

    def find(self, id):
        
        collection = 'boats'

        result = urlopen('http://localhost:1881/api/{0}/fields=name&where=id:\'{1}\''.format(collection, id))
        return json.loads(result.read())[collection]

    def test_boats_create(self):
        
        name = 'Watermelon'
        new_name = 'Avocado'

        # create

        created = self.create(['boat(name,id)'], {'name': '\'' + name + '\'', 'capacity': 120})

        assert created['name'] == name

        print('Created: {0}'.format(created))

        assert self.find(created['id'])[0]['name'] == name

        print('Found in store')

        # update

        updated = self.update(['boats(name,id)'], {'id': '\'' + created['id'] + '\''}, {'name': '\'' + new_name + '\''})[0]

        assert updated['name'] == new_name

        print('Updated: {0}'.format(updated))

        assert self.find(created['id'])[0]['name'] == new_name

        print('Found updated in store')

        # remove

        removed = self.remove(['boat(name,id)'], {'id': '\'' + created['id'] + '\''})

        assert removed['name'] == new_name

        print('Removed: {0}'.format(removed))

        assert len(self.find(created['id'])) == 0

        print('Not found in store')

        

if __name__ == '__main__':
    unittest.main()
import unittest
from urllib.request import urlopen
import json

SINGULAR = 'location'
PLURAL = 'locations'

FIELDS_TO_SHOW = 'name,id'
CHECKING_PARAM = 'name'

FIRST_VALUE = 'Watermelon'
SECOND_VALUE = 'Avocado'

CREATE_PARAMS = {CHECKING_PARAM: '\'' + FIRST_VALUE + '\''}
UPDATE_PARAMS = {CHECKING_PARAM: '\'' + SECOND_VALUE + '\''}

def sliceindex(x):
    i = 0
    for c in x:
        if c.isalpha():
            i = i + 1
            return i
        i = i + 1

def upperfirst(x):
    i = sliceindex(x)
    return x[:i].upper() + x[i:]

##

class TestCrud(unittest.TestCase):

    def switch_existential_state(self, operation, fields, where):
        path = 'http://localhost:1881/api/{0}/{3}/fields={1}&where={2}'.format(operation, ','.join(fields), 
            ','.join([str(key) + ':' + str(where[key]) for key in where]), SINGULAR).replace(' ','%20')

        #print(path)

        result = urlopen(str(path), timeout = 10)

        return json.loads(result.read())['{0}{1}'.format(operation, upperfirst(SINGULAR))][SINGULAR]

    def create(self, fields, where):
        return self.switch_existential_state('create', fields, where)

    def remove(self, fields, where):
        return self.switch_existential_state('remove', fields, where)

    def update(self, fields, where, set_fields):

        collection = SINGULAR

        path = 'http://localhost:1881/api/{0}/fields={1}&where={2}&set={3}'.format(collection, ','.join(fields), 
            ','.join([str(key) + ':' + str(where[key]) for key in where]),
            ','.join([str(key) + ':' + str(set_fields[key]) for key in set_fields])).replace(' ', '%20')

        #print(path)
        
        result = urlopen(path)

        return json.loads(result.read())['update{0}'.format(upperfirst(SINGULAR))]['ok']

    def find(self, date, time):
        
        collection = SINGULAR

        path = 'http://localhost:1881/api/{0}/fields={3}&where=date:\'{1}\'&time:\'{2}\''.format(collection, date, time, FIELDS_TO_SHOW)

        #print(path)

        result = urlopen(path)
        return json.loads(result.read())[collection]

    def test_crud(self):

        # create

        created = self.create(['{0}({1})'.format(SINGULAR, FIELDS_TO_SHOW)], CREATE_PARAMS)

        assert created[CHECKING_PARAM] == FIRST_VALUE

        print('Created: {0}'.format(created))

        assert self.find(created['date'], created['time'])[0][CHECKING_PARAM] == FIRST_VALUE

        print('Found in store')

        # update

        updated = self.update(['ok'], {'timestamp': '\'' + created['date'] + ' ' + created['time'] + '\''}, 
            UPDATE_PARAMS)

        assert updated

        print('Updated: {0}'.format(updated))

        assert self.find(created['date'], created['time'])[0][CHECKING_PARAM] == SECOND_VALUE

        print('Found updated in store')

        # remove

        removed = self.remove(['{0}({1})'.format(SINGULAR, FIELDS_TO_SHOW)], {'timestamp': '\'' + created['date'] + ' ' + created['time'] + '\''})

        assert removed[CHECKING_PARAM] == SECOND_VALUE

        print('Removed: {0}'.format(removed))

        assert len(self.find(created['date'], created['time'])) == 0

        print('Not found in store')
        

if __name__ == '__main__':
    unittest.main()
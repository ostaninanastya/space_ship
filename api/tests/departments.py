import unittest
from urllib.request import urlopen
import json

MIN = 3

class TestDepartmentsCrud(unittest.TestCase):

    def switch_existential_state(self, operation, fields, where):
        result = urlopen('http://localhost:1881/api/{0}/department/fields={1}&where={2}'.format(operation, ','.join(fields), 
            ','.join([str(key) + ':' + str(where[key]) for key in where])))
        return json.loads(result.read())['{0}Department'.format(operation)]['department']

    def create(self, fields, where):
        return self.switch_existential_state('create', fields, where)

    def remove(self, fields, where):
        return self.switch_existential_state('remove', fields, where)

    def update(self, fields, where, set_fields):

        collection = 'departments'
        
        result = urlopen('http://localhost:1881/api/{0}/fields={1}&where={2}&set={3}'.format(collection, ','.join(fields), 
            ','.join([str(key) + ':' + str(where[key]) for key in where]),
            ','.join([str(key) + ':' + str(set_fields[key]) for key in set_fields])))

        return json.loads(result.read())['updateDepartments']['departments']

    def find(self, id):
        
        collection = 'departments'

        result = urlopen('http://localhost:1881/api/{0}/fields=name&where=id:\'{1}\''.format(collection, id))
        return json.loads(result.read())[collection]

    def test_departments_crud(self):
        
        name = 'Watermelon'
        new_name = 'Avocado'

        # create

        created = self.create(['department(name,id)'], {'name': '\'' + name + '\'', 'vk': "'dep'"})

        assert created['name'] == name

        print('Created: {0}'.format(created))

        assert self.find(created['id'])[0]['name'] == name

        print('Found in store')

        # update

        updated = self.update(['departments(name,id)'], {'id': '\'' + created['id'] + '\''}, {'name': '\'' + new_name + '\''})[0]

        assert updated['name'] == new_name

        print('Updated: {0}'.format(updated))

        assert self.find(created['id'])[0]['name'] == new_name

        print('Found updated in store')

        # remove

        removed = self.remove(['department(name,id)'], {'id': '\'' + created['id'] + '\''})

        assert removed['name'] == new_name

        print('Removed: {0}'.format(removed))

        assert len(self.find(created['id'])) == 0

        print('Not found in store')

        

if __name__ == '__main__':
    unittest.main()
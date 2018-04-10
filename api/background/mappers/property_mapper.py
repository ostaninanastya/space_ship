import sys, os
import graphene

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/')

import mongo_native

from property_type_mapper import PropertyTypeMapper
from department_mapper import DepartmentMapper

class PropertyMapper(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    type = graphene.Field(lambda: PropertyTypeMapper)
    admission = graphene.String()
    comissioning = graphene.String()
    department = graphene.Field(lambda: DepartmentMapper)

    def resolve_type(self, info):
        return PropertyTypeMapper.init_scalar(mongo_native.get_property_type_by_id(self.type))

    def resolve_department(self, info):
        return DepartmentMapper(id = self.department)

    @staticmethod
    def init_scalar(item):
        return PropertyMapper(id = str(item['_id']), name = item['name'], department = item['department'], type = item['type'], comissioning = str(item['comissioning']), admission = str(item['admission']))

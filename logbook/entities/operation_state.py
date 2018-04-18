import sys, os
from datetime import datetime
import math

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import ValidationError

sys.path.append('adapters')

import neo4j_adapter
import mongo_adapter
from data_adapters import get_strings

OPERATION_STATUSES = get_strings(os.environ['SPACE_SHIP_HOME'] + '/logbook/enums/operation_statuses')
CHEMICAL_ELEMENTS = get_strings(os.environ['SPACE_SHIP_HOME'] + '/logbook/enums/chemical_elements')

class OperationState(Model):
    date = columns.Date(required = True, partition_key = True)
    time = columns.Time(required = True, primary_key = True)
    
    boat_id = columns.Bytes()
    operation_id = columns.Bytes(required = True)
    
    operation_status = columns.Text(required = True)
    
    distance_to_the_ship = columns.Double(required = True)
    zenith = columns.Double(required = True)
    azimuth = columns.Double(required = True)

    hydrogenium = columns.Double(required = True)
    helium = columns.Double(required = True)
    lithium = columns.Double(required = True)
    beryllium = columns.Double(required = True)
    borum = columns.Double(required = True)
    carboneum = columns.Double(required = True)
    nitrogenium = columns.Double(required = True)
    oxygenium = columns.Double(required = True)
    fluorum = columns.Double(required = True)
    neon = columns.Double(required = True)
    natrium = columns.Double(required = True)
    magnesium = columns.Double(required = True)
    aluminium = columns.Double(required = True)
    silicium = columns.Double(required = True)
    phosphorus = columns.Double(required = True)
    sulfur = columns.Double(required = True)
    chlorum = columns.Double(required = True)
    argon = columns.Double(required = True)
    kalium = columns.Double(required = True)
    calcium = columns.Double(required = True)
    scandium = columns.Double(required = True)
    titanium = columns.Double(required = True)
    vanadium = columns.Double(required = True)
    chromium = columns.Double(required = True)
    manganum  = columns.Double(required = True)
    ferrum = columns.Double(required = True)
    cobaltum = columns.Double(required = True)
    niccolum = columns.Double(required = True)
    cuprum = columns.Double(required = True)
    zincum = columns.Double(required = True)
    gallium = columns.Double(required = True)
    germanium = columns.Double(required = True)
    arsenicum = columns.Double(required = True)
    selenium = columns.Double(required = True)
    bromum = columns.Double(required = True)
    crypton = columns.Double(required = True)
    rubidium = columns.Double(required = True)
    strontium = columns.Double(required = True)
    yttrium = columns.Double(required = True)
    zirconium = columns.Double(required = True)
    niobium = columns.Double(required = True)
    molybdaenum = columns.Double(required = True)
    technetium = columns.Double(required = True)
    ruthenium = columns.Double(required = True)
    rhodium = columns.Double(required = True)
    palladium = columns.Double(required = True)
    argentum = columns.Double(required = True)
    cadmium = columns.Double(required = True)
    indium = columns.Double(required = True)
    stannum = columns.Double(required = True)
    stibium = columns.Double(required = True)
    tellurium = columns.Double(required = True)
    iodium = columns.Double(required = True)
    xenon = columns.Double(required = True)
    caesium = columns.Double(required = True)
    barium = columns.Double(required = True)
    lanthanum = columns.Double(required = True)
    cerium = columns.Double(required = True)
    praseodymium = columns.Double(required = True)
    neodymium = columns.Double(required = True)
    promethium = columns.Double(required = True)
    samarium = columns.Double(required = True)
    europium = columns.Double(required = True)
    gadolinium = columns.Double(required = True)
    terbium = columns.Double(required = True)
    dysprosium = columns.Double(required = True)
    holmium = columns.Double(required = True)
    erbium = columns.Double(required = True)
    thulium = columns.Double(required = True)
    ytterbium = columns.Double(required = True)
    lutetium = columns.Double(required = True)
    hafnium = columns.Double(required = True)
    tantalum = columns.Double(required = True)
    wolframium = columns.Double(required = True)
    rhenium = columns.Double(required = True)
    osmium = columns.Double(required = True)
    iridium = columns.Double(required = True)
    platinum = columns.Double(required = True)
    aurum = columns.Double(required = True)
    hydrargyrum = columns.Double(required = True)
    thallium = columns.Double(required = True)
    plumbum = columns.Double(required = True)
    bismuthum = columns.Double(required = True)
    polonium = columns.Double(required = True)
    astatum = columns.Double(required = True)
    radon = columns.Double(required = True)
    francium = columns.Double(required = True)
    radium = columns.Double(required = True)
    actinium = columns.Double(required = True)
    thorium = columns.Double(required = True)
    protactinium = columns.Double(required = True)
    uranium = columns.Double(required = True)
    neptunium = columns.Double(required = True)
    plutonium = columns.Double(required = True)
    americium = columns.Double(required = True)
    curium = columns.Double(required = True)
    berkelium = columns.Double(required = True)
    californium = columns.Double(required = True)
    einsteinium = columns.Double(required = True)
    fermium = columns.Double(required = True)
    mendelevium  = columns.Double(required = True)
    nobelium = columns.Double(required = True)
    lawrencium  = columns.Double(required = True)
    rutherfordium = columns.Double(required = True)
    dubnium = columns.Double(required = True)
    seaborgium = columns.Double(required = True)
    bohrium = columns.Double(required = True)
    hassium = columns.Double(required = True)
    meitnerium = columns.Double(required = True)
    darmstadtium = columns.Double(required = True)
    roentgenium = columns.Double(required = True)
    copernicium = columns.Double(required = True)
    nihonium = columns.Double(required = True)
    flerovium = columns.Double(required = True)
    moscovium = columns.Double(required = True)
    livermorium = columns.Double(required = True)
    tennessium = columns.Double(required = True)
    oganesson = columns.Double(required = True)
    
    comment = columns.Text()

    def validate(self):
        super(OperationState, self).validate()

        OperationState.validate_boat_id(self.boat_id)
        OperationState.validate_operation_id(self.operation_id)
        OperationState.validate_operation_status(self.operation_status)
        OperationState.validate_angle(self.zenith)
        OperationState.validate_angle(self.azimuth)
        OperationState.validate_elements_quantities([self[element] for element in CHEMICAL_ELEMENTS])
        OperationState.validate_comment(self.comment)

    @staticmethod
    def validate_boat_id(boat_id):
        if boat_id and (len(boat_id) != 12 or not mongo_adapter.is_valid_foreign_id('boat_test', boat_id.hex())):
            raise ValidationError('not a valid boat id')
        return boat_id

    @staticmethod
    def validate_operation_id(operation_id):
        if len(operation_id) != 16 or not neo4j_adapter.is_valid_foreign_id('Operation', operation_id.hex()):
            raise ValidationError('not a valid operation id')
        return operation_id

    @staticmethod
    def validate_operation_status(operation_status):
        if operation_status not in OPERATION_STATUSES:
            raise ValidationError('not an operation status')
        return operation_status

    @staticmethod
    def validate_angle(angle):
        angle -= math.floor(angle / (2 * math.pi)) * 2 * math.pi
        return angle

    @staticmethod
    def validate_elements_quantities(elements_quantities):
        elements_quantity_sum = 0

        for element in elements_quantities:
            if element < 0:
                raise ValidationError('invalid element quantity')
            elements_quantity_sum += element

        if abs(elements_quantity_sum - 100) > 0.1:
            raise ValidationError('invalid elements quantity')

        return elements_quantities
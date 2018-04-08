import sys, os
import graphene
from neomodel import config
from person_mapper import PersonMapper
from operation_mapper import OperationMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook/adapters/')

import mongo_adapter
import neo4j_adapter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/relations/entities/')

from operation import Operation

import configparser

configp = configparser.ConfigParser()
configp.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

NEO4J_DB_URL = os.environ.get('NEO4J_DB_URL') if os.environ.get('NEO4J_DB_URL') else configp['NEO4J']['host']
NEO4J_DB_PORT = int(os.environ.get('NEO4J_DB_PORT') if os.environ.get('NEO4J_DB_PORT') else configp['NEO4J']['port'])

USERNAME = os.environ.get('NEO4J_DB_USERNAME') if os.environ.get('NEO4J_DB_USERNAME') else configp['NEO4J']['username']
PASSWORD = os.environ.get('NEO4J_DB_PASSWORD') if os.environ.get('NEO4J_DB_PASSWORD') else configp['NEO4J']['password']

config.DATABASE_URL = 'bolt://' + USERNAME + ':' + PASSWORD + '@' + NEO4J_DB_URL + ':' + str(NEO4J_DB_PORT)

class OperationStateMapper(graphene.ObjectType):
    date = graphene.String()
    time = graphene.String()
    
    boatid = graphene.String()
    boatname = graphene.String()
    operationid = graphene.String()
    #operationname = graphene.String()
    #directorid = graphene.String()
    #directorname = graphene.String()
    operation = graphene.Field(OperationMapper)
    
    operationstatus = graphene.String()
    
    distancetotheship = graphene.Float()
    zenith = graphene.Float()
    azimuth = graphene.Float()

    hydrogenium = graphene.Float()
    helium = graphene.Float()
    lithium = graphene.Float()
    beryllium = graphene.Float()
    borum = graphene.Float()
    carboneum = graphene.Float()
    nitrogenium = graphene.Float()
    oxygenium = graphene.Float()
    fluorum = graphene.Float()
    neon = graphene.Float()
    natrium = graphene.Float()
    magnesium = graphene.Float()
    aluminium = graphene.Float()
    silicium = graphene.Float()
    phosphorus = graphene.Float()
    sulfur = graphene.Float()
    chlorum = graphene.Float()
    argon = graphene.Float()
    kalium = graphene.Float()
    calcium = graphene.Float()
    scandium = graphene.Float()
    titanium = graphene.Float()
    vanadium = graphene.Float()
    chromium = graphene.Float()
    manganum  = graphene.Float()
    ferrum = graphene.Float()
    cobaltum = graphene.Float()
    niccolum = graphene.Float()
    cuprum = graphene.Float()
    zincum = graphene.Float()
    gallium = graphene.Float()
    germanium = graphene.Float()
    arsenicum = graphene.Float()
    selenium = graphene.Float()
    bromum = graphene.Float()
    crypton = graphene.Float()
    rubidium = graphene.Float()
    strontium = graphene.Float()
    yttrium = graphene.Float()
    zirconium = graphene.Float()
    niobium = graphene.Float()
    molybdaenum = graphene.Float()
    technetium = graphene.Float()
    ruthenium = graphene.Float()
    rhodium = graphene.Float()
    palladium = graphene.Float()
    argentum = graphene.Float()
    cadmium = graphene.Float()
    indium = graphene.Float()
    stannum = graphene.Float()
    stibium = graphene.Float()
    tellurium = graphene.Float()
    iodium = graphene.Float()
    xenon = graphene.Float()
    caesium = graphene.Float()
    barium = graphene.Float()
    lanthanum = graphene.Float()
    cerium = graphene.Float()
    praseodymium = graphene.Float()
    neodymium = graphene.Float()
    promethium = graphene.Float()
    samarium = graphene.Float()
    europium = graphene.Float()
    gadolinium = graphene.Float()
    terbium = graphene.Float()
    dysprosium = graphene.Float()
    holmium = graphene.Float()
    erbium = graphene.Float()
    thulium = graphene.Float()
    ytterbium = graphene.Float()
    lutetium = graphene.Float()
    hafnium = graphene.Float()
    tantalum = graphene.Float()
    wolframium = graphene.Float()
    rhenium = graphene.Float()
    osmium = graphene.Float()
    iridium = graphene.Float()
    platinum = graphene.Float()
    aurum = graphene.Float()
    hydrargyrum = graphene.Float()
    thallium = graphene.Float()
    plumbum = graphene.Float()
    bismuthum = graphene.Float()
    polonium = graphene.Float()
    astatum = graphene.Float()
    radon = graphene.Float()
    francium = graphene.Float()
    radium = graphene.Float()
    actinium = graphene.Float()
    thorium = graphene.Float()
    protactinium = graphene.Float()
    uranium = graphene.Float()
    neptunium = graphene.Float()
    plutonium = graphene.Float()
    americium = graphene.Float()
    curium = graphene.Float()
    berkelium = graphene.Float()
    californium = graphene.Float()
    einsteinium = graphene.Float()
    fermium = graphene.Float()
    mendelevium  = graphene.Float()
    nobelium = graphene.Float()
    lawrencium  = graphene.Float()
    rutherfordium = graphene.Float()
    dubnium = graphene.Float()
    seaborgium = graphene.Float()
    bohrium = graphene.Float()
    hassium = graphene.Float()
    meitnerium = graphene.Float()
    darmstadtium = graphene.Float()
    roentgenium = graphene.Float()
    copernicium = graphene.Float()
    nihonium = graphene.Float()
    flerovium = graphene.Float()
    moscovium = graphene.Float()
    livermorium = graphene.Float()
    tennessium = graphene.Float()
    oganesson = graphene.Float()
    
    comment = graphene.String()

    def resolve_operation(self, info):

    	node = Operation.nodes.get(ident = self.operationid)

    	return OperationMapper(id = node.ident,\
    						   name = node.name,\
        					   start = str(node.start),\
        					   end = str(node.end))
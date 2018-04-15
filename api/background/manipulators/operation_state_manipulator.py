import sys, os
import configparser
import datetime
import graphene
import numpy as np

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from operation_state_mapper import OperationStateMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

import cassandra_mediator

config = configparser.ConfigParser()
config.read(os.environ['SPACE_SHIP_HOME'] + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']

class CreateOperationState(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()
        boat = graphene.String(default_value = '')
        operation = graphene.String()
    
        status = graphene.String()
    
        distancetotheship = graphene.Float()
        zenith = graphene.Float()
        azimuth = graphene.Float()

        hydrogenium = graphene.Float(default_value = 0)
        helium = graphene.Float(default_value = 0)
        lithium = graphene.Float(default_value = 0)
        beryllium = graphene.Float(default_value = 0)
        borum = graphene.Float(default_value = 0)
        carboneum = graphene.Float(default_value = 0)
        nitrogenium = graphene.Float(default_value = 0)
        oxygenium = graphene.Float(default_value = 0)
        fluorum = graphene.Float(default_value = 0)
        neon = graphene.Float(default_value = 0)
        natrium = graphene.Float(default_value = 0)
        magnesium = graphene.Float(default_value = 0)
        aluminium = graphene.Float(default_value = 0)
        silicium = graphene.Float(default_value = 0)
        phosphorus = graphene.Float(default_value = 0)
        sulfur = graphene.Float(default_value = 0)
        chlorum = graphene.Float(default_value = 0)
        argon = graphene.Float(default_value = 0)
        kalium = graphene.Float(default_value = 0)
        calcium = graphene.Float(default_value = 0)
        scandium = graphene.Float(default_value = 0)
        titanium = graphene.Float(default_value = 0)
        vanadium = graphene.Float(default_value = 0)
        chromium = graphene.Float(default_value = 0)
        manganum  = graphene.Float(default_value = 0)
        ferrum = graphene.Float(default_value = 0)
        cobaltum = graphene.Float(default_value = 0)
        niccolum = graphene.Float(default_value = 0)
        cuprum = graphene.Float(default_value = 0)
        zincum = graphene.Float(default_value = 0)
        gallium = graphene.Float(default_value = 0)
        germanium = graphene.Float(default_value = 0)
        arsenicum = graphene.Float(default_value = 0)
        selenium = graphene.Float(default_value = 0)
        bromum = graphene.Float(default_value = 0)
        crypton = graphene.Float(default_value = 0)
        rubidium = graphene.Float(default_value = 0)
        strontium = graphene.Float(default_value = 0)
        yttrium = graphene.Float(default_value = 0)
        zirconium = graphene.Float(default_value = 0)
        niobium = graphene.Float(default_value = 0)
        molybdaenum = graphene.Float(default_value = 0)
        technetium = graphene.Float(default_value = 0)
        ruthenium = graphene.Float(default_value = 0)
        rhodium = graphene.Float(default_value = 0)
        palladium = graphene.Float(default_value = 0)
        argentum = graphene.Float(default_value = 0)
        cadmium = graphene.Float(default_value = 0)
        indium = graphene.Float(default_value = 0)
        stannum = graphene.Float(default_value = 0)
        stibium = graphene.Float(default_value = 0)
        tellurium = graphene.Float(default_value = 0)
        iodium = graphene.Float(default_value = 0)
        xenon = graphene.Float(default_value = 0)
        caesium = graphene.Float(default_value = 0)
        barium = graphene.Float(default_value = 0)
        lanthanum = graphene.Float(default_value = 0)
        cerium = graphene.Float(default_value = 0)
        praseodymium = graphene.Float(default_value = 0)
        neodymium = graphene.Float(default_value = 0)
        promethium = graphene.Float(default_value = 0)
        samarium = graphene.Float(default_value = 0)
        europium = graphene.Float(default_value = 0)
        gadolinium = graphene.Float(default_value = 0)
        terbium = graphene.Float(default_value = 0)
        dysprosium = graphene.Float(default_value = 0)
        holmium = graphene.Float(default_value = 0)
        erbium = graphene.Float(default_value = 0)
        thulium = graphene.Float(default_value = 0)
        ytterbium = graphene.Float(default_value = 0)
        lutetium = graphene.Float(default_value = 0)
        hafnium = graphene.Float(default_value = 0)
        tantalum = graphene.Float(default_value = 0)
        wolframium = graphene.Float(default_value = 0)
        rhenium = graphene.Float(default_value = 0)
        osmium = graphene.Float(default_value = 0)
        iridium = graphene.Float(default_value = 0)
        platinum = graphene.Float(default_value = 0)
        aurum = graphene.Float(default_value = 0)
        hydrargyrum = graphene.Float(default_value = 0)
        thallium = graphene.Float(default_value = 0)
        plumbum = graphene.Float(default_value = 0)
        bismuthum = graphene.Float(default_value = 0)
        polonium = graphene.Float(default_value = 0)
        astatum = graphene.Float(default_value = 0)
        radon = graphene.Float(default_value = 0)
        francium = graphene.Float(default_value = 0)
        radium = graphene.Float(default_value = 0)
        actinium = graphene.Float(default_value = 0)
        thorium = graphene.Float(default_value = 0)
        protactinium = graphene.Float(default_value = 0)
        uranium = graphene.Float(default_value = 0)
        neptunium = graphene.Float(default_value = 0)
        plutonium = graphene.Float(default_value = 0)
        americium = graphene.Float(default_value = 0)
        curium = graphene.Float(default_value = 0)
        berkelium = graphene.Float(default_value = 0)
        californium = graphene.Float(default_value = 0)
        einsteinium = graphene.Float(default_value = 0)
        fermium = graphene.Float(default_value = 0)
        mendelevium  = graphene.Float(default_value = 0)
        nobelium = graphene.Float(default_value = 0)
        lawrencium  = graphene.Float(default_value = 0)
        rutherfordium = graphene.Float(default_value = 0)
        dubnium = graphene.Float(default_value = 0)
        seaborgium = graphene.Float(default_value = 0)
        bohrium = graphene.Float(default_value = 0)
        hassium = graphene.Float(default_value = 0)
        meitnerium = graphene.Float(default_value = 0)
        darmstadtium = graphene.Float(default_value = 0)
        roentgenium = graphene.Float(default_value = 0)
        copernicium = graphene.Float(default_value = 0)
        nihonium = graphene.Float(default_value = 0)
        flerovium = graphene.Float(default_value = 0)
        moscovium = graphene.Float(default_value = 0)
        livermorium = graphene.Float(default_value = 0)
        tennessium = graphene.Float(default_value = 0)
        oganesson = graphene.Float(default_value = 0)
        
        comment = graphene.String()

    ok = graphene.Boolean()
    operationstate = graphene.Field(lambda: OperationStateMapper)

    def mutate(self, info, timestamp, boat, operation, status, distancetotheship, zenith, azimuth, hydrogenium, helium, lithium, beryllium, borum,\
    carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,\
    scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,\
    crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,\
    stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,\
    terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,\
    hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,\
    plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,\
    seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,\
    oganesson, comment):

        operationstate = OperationStateMapper.init_scalar(cassandra_mediator.create_operation_state(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN),\
            boat, operation, status, distancetotheship, zenith, azimuth, hydrogenium, helium, lithium, beryllium, borum,\
            carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,\
            scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,\
            crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,\
            stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,\
            terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,\
            hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,\
            plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,\
            seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,\
            oganesson, comment))
        ok = True
        return CreateOperationState(operationstate = operationstate, ok = ok)

class RemoveOperationState(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String()

    ok = graphene.Boolean()
    operationstate = graphene.Field(lambda: OperationStateMapper)

    def mutate(self, info, timestamp):
        operationstate = OperationStateMapper.init_scalar(cassandra_mediator.remove_operation_state(datetime.datetime.strptime(timestamp, TIMESTAMP_PATTERN)))
        ok = True
        return RemoveOperationState(operationstate = operationstate, ok = ok)
import sys, os
import configparser
import datetime
import graphene
import numpy as np

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/api/background/mappers')

from operation_state_mapper import OperationStateMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_bytes_parameter, parse_timestamp_parameter, stringify_timestamp_parameter, parse_objectid_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class CreateOperationState(graphene.Mutation):
    class Arguments:

        timestamp = graphene.String()
        boat = graphene.String(default_value = '')
        operation = graphene.String()
    
        status = graphene.String()
    
        distance = graphene.Float()
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
    operation_state = graphene.Field(lambda: OperationStateMapper)

    def mutate(self, info, timestamp, boat, operation, status, distance, zenith, azimuth, hydrogenium, helium, lithium, beryllium, borum,\
    carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,\
    scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,\
    crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,\
    stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,\
    terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,\
    hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,\
    plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,\
    seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,\
    oganesson, comment):

        operation_state = OperationStateMapper.init_scalar(mongo_mediator.create_operation_state(parse_timestamp_parameter(timestamp),\
            parse_objectid_parameter(boat), parse_objectid_parameter(operation), status, distance, zenith, azimuth, hydrogenium, helium, 
            lithium, beryllium, borum,
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
        return CreateOperationState(operation_state = operation_state, ok = ok)

class RemoveOperationState(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    operation_state = graphene.Field(lambda: OperationStateMapper)

    def mutate(self, info, timestamp):
        operation_state = OperationStateMapper.init_scalar(mongo_mediator.remove_operation_state(id))
        ok = True
        return RemoveOperationState(operation_state = operation_state, ok = ok)

class UpdateOperationStates(graphene.Mutation):
    class Arguments:

        id = graphene.String(default_value = '')
        timestamp = graphene.String(default_value = '')
        boat = graphene.String(default_value = '')
        operation = graphene.String(default_value = '')
        status = graphene.String(default_value = '')
        distance = graphene.Float(default_value = float('nan'))
        zenith = graphene.Float(default_value = float('nan'))
        azimuth = graphene.Float(default_value = float('nan'))
        hydrogenium = graphene.Float(default_value = float('nan'))
        helium = graphene.Float(default_value = float('nan'))
        lithium = graphene.Float(default_value = float('nan'))
        beryllium = graphene.Float(default_value = float('nan'))
        borum = graphene.Float(default_value = float('nan'))
        carboneum = graphene.Float(default_value = float('nan'))
        nitrogenium = graphene.Float(default_value = float('nan'))
        oxygenium = graphene.Float(default_value = float('nan'))
        fluorum = graphene.Float(default_value = float('nan'))
        neon = graphene.Float(default_value = float('nan'))
        natrium = graphene.Float(default_value = float('nan'))
        magnesium = graphene.Float(default_value = float('nan'))
        aluminium = graphene.Float(default_value = float('nan'))
        silicium = graphene.Float(default_value = float('nan'))
        phosphorus = graphene.Float(default_value = float('nan'))
        sulfur = graphene.Float(default_value = float('nan'))
        chlorum = graphene.Float(default_value = float('nan'))
        argon = graphene.Float(default_value = float('nan'))
        kalium = graphene.Float(default_value = float('nan'))
        calcium = graphene.Float(default_value = float('nan'))
        scandium = graphene.Float(default_value = float('nan'))
        titanium = graphene.Float(default_value = float('nan'))
        vanadium = graphene.Float(default_value = float('nan'))
        chromium = graphene.Float(default_value = float('nan'))
        manganum  = graphene.Float(default_value = float('nan'))
        ferrum = graphene.Float(default_value = float('nan'))
        cobaltum = graphene.Float(default_value = float('nan'))
        niccolum = graphene.Float(default_value = float('nan'))
        cuprum = graphene.Float(default_value = float('nan'))
        zincum = graphene.Float(default_value = float('nan'))
        gallium = graphene.Float(default_value = float('nan'))
        germanium = graphene.Float(default_value = float('nan'))
        arsenicum = graphene.Float(default_value = float('nan'))
        selenium = graphene.Float(default_value = float('nan'))
        bromum = graphene.Float(default_value = float('nan'))
        crypton = graphene.Float(default_value = float('nan'))
        rubidium = graphene.Float(default_value = float('nan'))
        strontium = graphene.Float(default_value = float('nan'))
        yttrium = graphene.Float(default_value = float('nan'))
        zirconium = graphene.Float(default_value = float('nan'))
        niobium = graphene.Float(default_value = float('nan'))
        molybdaenum = graphene.Float(default_value = float('nan'))
        technetium = graphene.Float(default_value = float('nan'))
        ruthenium = graphene.Float(default_value = float('nan'))
        rhodium = graphene.Float(default_value = float('nan'))
        palladium = graphene.Float(default_value = float('nan'))
        argentum = graphene.Float(default_value = float('nan'))
        cadmium = graphene.Float(default_value = float('nan'))
        indium = graphene.Float(default_value = float('nan'))
        stannum = graphene.Float(default_value = float('nan'))
        stibium = graphene.Float(default_value = float('nan'))
        tellurium = graphene.Float(default_value = float('nan'))
        iodium = graphene.Float(default_value = float('nan'))
        xenon = graphene.Float(default_value = float('nan'))
        caesium = graphene.Float(default_value = float('nan'))
        barium = graphene.Float(default_value = float('nan'))
        lanthanum = graphene.Float(default_value = float('nan'))
        cerium = graphene.Float(default_value = float('nan'))
        praseodymium = graphene.Float(default_value = float('nan'))
        neodymium = graphene.Float(default_value = float('nan'))
        promethium = graphene.Float(default_value = float('nan'))
        samarium = graphene.Float(default_value = float('nan'))
        europium = graphene.Float(default_value = float('nan'))
        gadolinium = graphene.Float(default_value = float('nan'))
        terbium = graphene.Float(default_value = float('nan'))
        dysprosium = graphene.Float(default_value = float('nan'))
        holmium = graphene.Float(default_value = float('nan'))
        erbium = graphene.Float(default_value = float('nan'))
        thulium = graphene.Float(default_value = float('nan'))
        ytterbium = graphene.Float(default_value = float('nan'))
        lutetium = graphene.Float(default_value = float('nan'))
        hafnium = graphene.Float(default_value = float('nan'))
        tantalum = graphene.Float(default_value = float('nan'))
        wolframium = graphene.Float(default_value = float('nan'))
        rhenium = graphene.Float(default_value = float('nan'))
        osmium = graphene.Float(default_value = float('nan'))
        iridium = graphene.Float(default_value = float('nan'))
        platinum = graphene.Float(default_value = float('nan'))
        aurum = graphene.Float(default_value = float('nan'))
        hydrargyrum = graphene.Float(default_value = float('nan'))
        thallium = graphene.Float(default_value = float('nan'))
        plumbum = graphene.Float(default_value = float('nan'))
        bismuthum = graphene.Float(default_value = float('nan'))
        polonium = graphene.Float(default_value = float('nan'))
        astatum = graphene.Float(default_value = float('nan'))
        radon = graphene.Float(default_value = float('nan'))
        francium = graphene.Float(default_value = float('nan'))
        radium = graphene.Float(default_value = float('nan'))
        actinium = graphene.Float(default_value = float('nan'))
        thorium = graphene.Float(default_value = float('nan'))
        protactinium = graphene.Float(default_value = float('nan'))
        uranium = graphene.Float(default_value = float('nan'))
        neptunium = graphene.Float(default_value = float('nan'))
        plutonium = graphene.Float(default_value = float('nan'))
        americium = graphene.Float(default_value = float('nan'))
        curium = graphene.Float(default_value = float('nan'))
        berkelium = graphene.Float(default_value = float('nan'))
        californium = graphene.Float(default_value = float('nan'))
        einsteinium = graphene.Float(default_value = float('nan'))
        fermium = graphene.Float(default_value = float('nan'))
        mendelevium  = graphene.Float(default_value = float('nan'))
        nobelium = graphene.Float(default_value = float('nan'))
        lawrencium  = graphene.Float(default_value = float('nan'))
        rutherfordium = graphene.Float(default_value = float('nan'))
        dubnium = graphene.Float(default_value = float('nan'))
        seaborgium = graphene.Float(default_value = float('nan'))
        bohrium = graphene.Float(default_value = float('nan'))
        hassium = graphene.Float(default_value = float('nan'))
        meitnerium = graphene.Float(default_value = float('nan'))
        darmstadtium = graphene.Float(default_value = float('nan'))
        roentgenium = graphene.Float(default_value = float('nan'))
        copernicium = graphene.Float(default_value = float('nan'))
        nihonium = graphene.Float(default_value = float('nan'))
        flerovium = graphene.Float(default_value = float('nan'))
        moscovium = graphene.Float(default_value = float('nan'))
        livermorium = graphene.Float(default_value = float('nan'))
        tennessium = graphene.Float(default_value = float('nan'))
        oganesson = graphene.Float(default_value = float('nan'))
        comment = graphene.String(default_value = '')

        set_boat = graphene.String(default_value = '')
        set_operation = graphene.String(default_value = '')
        set_status = graphene.String(default_value = '')
        set_distance = graphene.Float(default_value = float('nan'))
        set_zenith = graphene.Float(default_value = float('nan'))
        set_azimuth = graphene.Float(default_value = float('nan'))
        set_hydrogenium = graphene.Float(default_value = float('nan'))
        set_helium = graphene.Float(default_value = float('nan'))
        set_lithium = graphene.Float(default_value = float('nan'))
        set_beryllium = graphene.Float(default_value = float('nan'))
        set_borum = graphene.Float(default_value = float('nan'))
        set_carboneum = graphene.Float(default_value = float('nan'))
        set_nitrogenium = graphene.Float(default_value = float('nan'))
        set_oxygenium = graphene.Float(default_value = float('nan'))
        set_fluorum = graphene.Float(default_value = float('nan'))
        set_neon = graphene.Float(default_value = float('nan'))
        set_natrium = graphene.Float(default_value = float('nan'))
        set_magnesium = graphene.Float(default_value = float('nan'))
        set_aluminium = graphene.Float(default_value = float('nan'))
        set_silicium = graphene.Float(default_value = float('nan'))
        set_phosphorus = graphene.Float(default_value = float('nan'))
        set_sulfur = graphene.Float(default_value = float('nan'))
        set_chlorum = graphene.Float(default_value = float('nan'))
        set_argon = graphene.Float(default_value = float('nan'))
        set_kalium = graphene.Float(default_value = float('nan'))
        set_calcium = graphene.Float(default_value = float('nan'))
        set_scandium = graphene.Float(default_value = float('nan'))
        set_titanium = graphene.Float(default_value = float('nan'))
        set_vanadium = graphene.Float(default_value = float('nan'))
        set_chromium = graphene.Float(default_value = float('nan'))
        set_manganum  = graphene.Float(default_value = float('nan'))
        set_ferrum = graphene.Float(default_value = float('nan'))
        set_cobaltum = graphene.Float(default_value = float('nan'))
        set_niccolum = graphene.Float(default_value = float('nan'))
        set_cuprum = graphene.Float(default_value = float('nan'))
        set_zincum = graphene.Float(default_value = float('nan'))
        set_gallium = graphene.Float(default_value = float('nan'))
        set_germanium = graphene.Float(default_value = float('nan'))
        set_arsenicum = graphene.Float(default_value = float('nan'))
        set_selenium = graphene.Float(default_value = float('nan'))
        set_bromum = graphene.Float(default_value = float('nan'))
        set_crypton = graphene.Float(default_value = float('nan'))
        set_rubidium = graphene.Float(default_value = float('nan'))
        set_strontium = graphene.Float(default_value = float('nan'))
        set_yttrium = graphene.Float(default_value = float('nan'))
        set_zirconium = graphene.Float(default_value = float('nan'))
        set_niobium = graphene.Float(default_value = float('nan'))
        set_molybdaenum = graphene.Float(default_value = float('nan'))
        set_technetium = graphene.Float(default_value = float('nan'))
        set_ruthenium = graphene.Float(default_value = float('nan'))
        set_rhodium = graphene.Float(default_value = float('nan'))
        set_palladium = graphene.Float(default_value = float('nan'))
        set_argentum = graphene.Float(default_value = float('nan'))
        set_cadmium = graphene.Float(default_value = float('nan'))
        set_indium = graphene.Float(default_value = float('nan'))
        set_stannum = graphene.Float(default_value = float('nan'))
        set_stibium = graphene.Float(default_value = float('nan'))
        set_tellurium = graphene.Float(default_value = float('nan'))
        set_iodium = graphene.Float(default_value = float('nan'))
        set_xenon = graphene.Float(default_value = float('nan'))
        set_caesium = graphene.Float(default_value = float('nan'))
        set_barium = graphene.Float(default_value = float('nan'))
        set_lanthanum = graphene.Float(default_value = float('nan'))
        set_cerium = graphene.Float(default_value = float('nan'))
        set_praseodymium = graphene.Float(default_value = float('nan'))
        set_neodymium = graphene.Float(default_value = float('nan'))
        set_promethium = graphene.Float(default_value = float('nan'))
        set_samarium = graphene.Float(default_value = float('nan'))
        set_europium = graphene.Float(default_value = float('nan'))
        set_gadolinium = graphene.Float(default_value = float('nan'))
        set_terbium = graphene.Float(default_value = float('nan'))
        set_dysprosium = graphene.Float(default_value = float('nan'))
        set_holmium = graphene.Float(default_value = float('nan'))
        set_erbium = graphene.Float(default_value = float('nan'))
        set_thulium = graphene.Float(default_value = float('nan'))
        set_ytterbium = graphene.Float(default_value = float('nan'))
        set_lutetium = graphene.Float(default_value = float('nan'))
        set_hafnium = graphene.Float(default_value = float('nan'))
        set_tantalum = graphene.Float(default_value = float('nan'))
        set_wolframium = graphene.Float(default_value = float('nan'))
        set_rhenium = graphene.Float(default_value = float('nan'))
        set_osmium = graphene.Float(default_value = float('nan'))
        set_iridium = graphene.Float(default_value = float('nan'))
        set_platinum = graphene.Float(default_value = float('nan'))
        set_aurum = graphene.Float(default_value = float('nan'))
        set_hydrargyrum = graphene.Float(default_value = float('nan'))
        set_thallium = graphene.Float(default_value = float('nan'))
        set_plumbum = graphene.Float(default_value = float('nan'))
        set_bismuthum = graphene.Float(default_value = float('nan'))
        set_polonium = graphene.Float(default_value = float('nan'))
        set_astatum = graphene.Float(default_value = float('nan'))
        set_radon = graphene.Float(default_value = float('nan'))
        set_francium = graphene.Float(default_value = float('nan'))
        set_radium = graphene.Float(default_value = float('nan'))
        set_actinium = graphene.Float(default_value = float('nan'))
        set_thorium = graphene.Float(default_value = float('nan'))
        set_protactinium = graphene.Float(default_value = float('nan'))
        set_uranium = graphene.Float(default_value = float('nan'))
        set_neptunium = graphene.Float(default_value = float('nan'))
        set_plutonium = graphene.Float(default_value = float('nan'))
        set_americium = graphene.Float(default_value = float('nan'))
        set_curium = graphene.Float(default_value = float('nan'))
        set_berkelium = graphene.Float(default_value = float('nan'))
        set_californium = graphene.Float(default_value = float('nan'))
        set_einsteinium = graphene.Float(default_value = float('nan'))
        set_fermium = graphene.Float(default_value = float('nan'))
        set_mendelevium  = graphene.Float(default_value = float('nan'))
        set_nobelium = graphene.Float(default_value = float('nan'))
        set_lawrencium  = graphene.Float(default_value = float('nan'))
        set_rutherfordium = graphene.Float(default_value = float('nan'))
        set_dubnium = graphene.Float(default_value = float('nan'))
        set_seaborgium = graphene.Float(default_value = float('nan'))
        set_bohrium = graphene.Float(default_value = float('nan'))
        set_hassium = graphene.Float(default_value = float('nan'))
        set_meitnerium = graphene.Float(default_value = float('nan'))
        set_darmstadtium = graphene.Float(default_value = float('nan'))
        set_roentgenium = graphene.Float(default_value = float('nan'))
        set_copernicium = graphene.Float(default_value = float('nan'))
        set_nihonium = graphene.Float(default_value = float('nan'))
        set_flerovium = graphene.Float(default_value = float('nan'))
        set_moscovium = graphene.Float(default_value = float('nan'))
        set_livermorium = graphene.Float(default_value = float('nan'))
        set_tennessium = graphene.Float(default_value = float('nan'))
        set_oganesson = graphene.Float(default_value = float('nan'))
        set_comment = graphene.String(default_value = '')
        set_timestamp = graphene.String(default_value = '')

    ok = graphene.Boolean()

    def mutate(self, info, id, timestamp, boat, operation, status, distance, zenith, azimuth, hydrogenium, helium, lithium, beryllium, borum,\
    carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,\
    scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,\
    crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,\
    stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,\
    terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,\
    hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,\
    plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,\
    seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,\
    oganesson, comment, set_boat, set_operation, set_status, set_distance, set_zenith, set_azimuth, set_hydrogenium, set_helium,
    set_lithium, set_beryllium, set_borum, set_carboneum, set_nitrogenium, set_oxygenium, set_fluorum, set_neon, set_natrium, set_magnesium,
    set_aluminium, set_silicium, set_phosphorus, set_sulfur, set_chlorum, set_argon, set_kalium, set_calcium, set_scandium, set_titanium,
    set_vanadium, set_chromium, set_manganum, set_ferrum, set_cobaltum, set_niccolum, set_cuprum, set_zincum, set_gallium, set_germanium,
    set_arsenicum, set_selenium, set_bromum, set_crypton, set_rubidium, set_strontium, set_yttrium, set_zirconium, set_niobium, set_molybdaenum,
    set_technetium, set_ruthenium, set_rhodium, set_palladium, set_argentum, set_cadmium, set_indium, set_stannum, set_stibium, set_tellurium,
    set_iodium, set_xenon, set_caesium, set_barium, set_lanthanum, set_cerium, set_praseodymium, set_neodymium, set_promethium, set_samarium,
    set_europium, set_gadolinium, set_terbium, set_dysprosium, set_holmium, set_erbium, set_thulium, set_ytterbium, set_lutetium, set_hafnium,
    set_tantalum, set_wolframium, set_rhenium, set_osmium, set_iridium, set_platinum, set_aurum, set_hydrargyrum, set_thallium, set_plumbum,
    set_bismuthum, set_polonium, set_astatum, set_radon, set_francium, set_radium, set_actinium, set_thorium, set_protactinium, set_uranium,
    set_neptunium, set_plutonium, set_americium, set_curium, set_berkelium, set_californium, set_einsteinium, set_fermium, set_mendelevium,
    set_nobelium, set_lawrencium, set_rutherfordium, set_dubnium, set_seaborgium, set_bohrium, set_hassium, set_meitnerium, set_darmstadtium, 
    set_roentgenium, set_copernicium, set_nihonium, set_flerovium, set_moscovium, set_livermorium, set_tennessium, set_oganesson,set_comment, set_timestamp):
        operation_state = mongo_mediator.update_operation_states(id = parse_objectid_parameter(id), timestamp = parse_timestamp_parameter(timestamp),
            boat = parse_objectid_parameter(boat), operation = parse_objectid_parameter(boat), 
            status = status, zenith = zenith, azimuth = azimuth, comment = comment, distance = distance,
            set_boat = parse_objectid_parameter(set_boat), 
            set_operation = parse_objectid_parameter(set_operation), 
            set_status = set_status, set_distance = set_distance, set_zenith = set_zenith, set_azimuth = set_azimuth, set_comment = set_comment,
            set_timestamp = parse_timestamp_parameter(set_timestamp),
            set_hydrogenium = set_hydrogenium, hydrogenium = hydrogenium, set_helium = set_helium, helium = helium, 
            set_lithium = set_lithium, lithium = lithium, set_beryllium = set_beryllium, beryllium = beryllium, 
            set_borum = set_borum, borum = borum, set_carboneum = set_carboneum, carboneum = carboneum, set_nitrogenium = set_nitrogenium, 
            nitrogenium = nitrogenium, set_oxygenium = set_oxygenium, oxygenium = oxygenium, set_fluorum = set_fluorum, fluorum = fluorum, 
            set_neon = set_neon, neon = neon, set_natrium = set_natrium, natrium = natrium, set_magnesium = set_magnesium, magnesium = magnesium, 
            set_aluminium = set_aluminium, aluminium = aluminium, set_silicium = set_silicium, silicium = silicium, set_phosphorus = set_phosphorus, 
            phosphorus = phosphorus, set_sulfur = set_sulfur, sulfur = sulfur, set_chlorum = set_chlorum, chlorum = chlorum, set_argon = set_argon, 
            argon = argon, set_kalium = set_kalium, kalium = kalium, set_calcium = set_calcium, calcium = calcium, set_scandium = set_scandium, 
            scandium = scandium, set_titanium = set_titanium, titanium = titanium, set_vanadium = set_vanadium, vanadium = vanadium, 
            set_chromium = set_chromium, chromium = chromium, set_manganum = set_manganum, manganum = manganum, set_ferrum = set_ferrum, 
            ferrum = ferrum, set_cobaltum = set_cobaltum, cobaltum = cobaltum, set_niccolum = set_niccolum, niccolum = niccolum, 
            set_cuprum = set_cuprum, cuprum = cuprum, set_zincum = set_zincum, zincum = zincum, set_gallium = set_gallium, 
            gallium = gallium, set_germanium = set_germanium, germanium = germanium, set_arsenicum = set_arsenicum, 
            arsenicum = arsenicum, set_selenium = set_selenium, selenium = selenium, set_bromum = set_bromum, 
            bromum = bromum, set_crypton = set_crypton, crypton = crypton, set_rubidium = set_rubidium, rubidium = rubidium, 
            set_strontium = set_strontium, strontium = strontium, set_yttrium = set_yttrium, yttrium = yttrium, set_zirconium = set_zirconium, 
            zirconium = zirconium, set_niobium = set_niobium, niobium = niobium, set_molybdaenum = set_molybdaenum, molybdaenum = molybdaenum, 
            set_technetium = set_technetium, technetium = technetium, set_ruthenium = set_ruthenium, ruthenium = ruthenium, set_rhodium = set_rhodium, 
            rhodium = rhodium, set_palladium = set_palladium, palladium = palladium, set_argentum = set_argentum, argentum = argentum, 
            set_cadmium = set_cadmium, cadmium = cadmium, set_indium = set_indium, indium = indium, set_stannum = set_stannum, stannum = stannum, 
            set_stibium = set_stibium, stibium = stibium, set_tellurium = set_tellurium, tellurium = tellurium, set_iodium = set_iodium, 
            iodium = iodium, set_xenon = set_xenon, xenon = xenon, set_caesium = set_caesium, caesium = caesium, set_barium = set_barium, 
            barium = barium, set_lanthanum = set_lanthanum, lanthanum = lanthanum, set_cerium = set_cerium, cerium = cerium, 
            set_praseodymium = set_praseodymium, praseodymium = praseodymium, set_neodymium = set_neodymium, neodymium = neodymium, 
            set_promethium = set_promethium, promethium = promethium, set_samarium = set_samarium, samarium = samarium, set_europium = set_europium, 
            europium = europium, set_gadolinium = set_gadolinium, gadolinium = gadolinium, set_terbium = set_terbium, terbium = terbium, 
            set_dysprosium = set_dysprosium, dysprosium = dysprosium, set_holmium = set_holmium, holmium = holmium, set_erbium = set_erbium, 
            erbium = erbium, set_thulium = set_thulium, thulium = thulium, set_ytterbium = set_ytterbium, ytterbium = ytterbium, 
            set_lutetium = set_lutetium, lutetium = lutetium, set_hafnium = set_hafnium, hafnium = hafnium, set_tantalum = set_tantalum, 
            tantalum = tantalum, set_wolframium = set_wolframium, wolframium = wolframium, set_rhenium = set_rhenium, rhenium = rhenium, 
            set_osmium = set_osmium, osmium = osmium, set_iridium = set_iridium, iridium = iridium, set_platinum = set_platinum, platinum = platinum, 
            set_aurum = set_aurum, aurum = aurum, set_hydrargyrum = set_hydrargyrum, hydrargyrum = hydrargyrum, set_thallium = set_thallium, 
            thallium = thallium, set_plumbum = set_plumbum, plumbum = plumbum, set_bismuthum = set_bismuthum, bismuthum = bismuthum, 
            set_polonium = set_polonium, polonium = polonium, set_astatum = set_astatum, astatum = astatum, set_radon = set_radon, radon = radon, 
            set_francium = set_francium, francium = francium, set_radium = set_radium, radium = radium, set_actinium = set_actinium, actinium = actinium, 
            set_thorium = set_thorium, thorium = thorium, set_protactinium = set_protactinium, protactinium = protactinium, set_uranium = set_uranium, 
            uranium = uranium, set_neptunium = set_neptunium, neptunium = neptunium, set_plutonium = set_plutonium, plutonium = plutonium,
            set_americium = set_americium, americium = americium, set_curium = set_curium, curium = curium, set_berkelium = set_berkelium, 
            berkelium = berkelium, set_californium = set_californium, californium = californium, set_einsteinium = set_einsteinium, einsteinium = einsteinium, 
            set_fermium = set_fermium, fermium = fermium, set_mendelevium = set_mendelevium, mendelevium = mendelevium, set_nobelium = set_nobelium, 
            nobelium = nobelium, set_lawrencium = set_lawrencium, lawrencium = lawrencium, set_rutherfordium = set_rutherfordium, 
            rutherfordium = rutherfordium, set_dubnium = set_dubnium, dubnium = dubnium, set_seaborgium = set_seaborgium, seaborgium = seaborgium, 
            set_bohrium = set_bohrium, bohrium = bohrium, set_hassium = set_hassium, hassium = hassium, set_meitnerium = set_meitnerium, 
            meitnerium = meitnerium, set_darmstadtium = set_darmstadtium, darmstadtium = darmstadtium, set_roentgenium = set_roentgenium, 
            roentgenium = roentgenium, set_copernicium = set_copernicium, copernicium = copernicium, set_nihonium = set_nihonium, nihonium = nihonium, 
            set_flerovium = set_flerovium, flerovium = flerovium, set_moscovium = set_moscovium, moscovium = moscovium, set_livermorium = set_livermorium, 
            livermorium = livermorium, set_tennessium = set_tennessium, tennessium = tennessium, set_oganesson = set_oganesson, oganesson = oganesson)
        ok = True
        return UpdateOperationStates(ok = ok)
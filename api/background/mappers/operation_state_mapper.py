import sys, os, datetime
import graphene
from neomodel import config
from person_mapper import PersonMapper
from operation_mapper import OperationMapper
from boat_mapper import BoatMapper

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/logbook')

from data_adapters import parse_bytes_parameter, parse_timestamp_parameter, stringify_timestamp_parameter, parse_objectid_parameter

sys.path.append(os.environ['SPACE_SHIP_HOME'] + '/recital/')

import mongo_mediator

class OperationStateMapper(graphene.ObjectType):
    
    id = graphene.String()
    timestamp = graphene.String()
    
    boat = graphene.Field(lambda: BoatMapper)
    operation = graphene.Field(lambda: OperationMapper)
    status = graphene.String()
    distance = graphene.Float()
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
    	return OperationMapper.init_scalar(mongo_mediator.get_operation_by_id(self.operation))

    def resolve_boat(self, info):
      return BoatMapper.init_scalar(mongo_mediator.get_boat_by_id(self.boat))

    @staticmethod
    def eject(id, timestamp, boat, operation, status, distance, zenith, azimuth, hydrogenium,
        helium, lithium, beryllium, borum,
        carboneum, nitrogenium, oxygenium, fluorum, neon, natrium, magnesium, aluminium, silicium, phosphorus, sulfur, chlorum, argon, kalium, calcium,
        scandium, titanium, vanadium, chromium, manganum, ferrum, cobaltum, niccolum, cuprum, zincum, gallium, germanium, arsenicum, selenium, bromum,
        crypton, rubidium, strontium, yttrium, zirconium, niobium, molybdaenum, technetium, ruthenium, rhodium, palladium, argentum, cadmium, indium,
        stannum, stibium, tellurium, iodium, xenon, caesium, barium, lanthanum, cerium, praseodymium, neodymium, promethium, samarium, europium, gadolinium,
        terbium, dysprosium, holmium, erbium, thulium, ytterbium, lutetium, hafnium, tantalum, wolframium, rhenium, osmium, iridium, platinum, aurum,
        hydrargyrum, thallium, plumbum, bismuthum, polonium, astatum, radon, francium, radium, actinium, thorium, protactinium, uranium, neptunium,
        plutonium, americium, curium, berkelium, californium, einsteinium, fermium, mendelevium, nobelium, lawrencium, rutherfordium, dubnium,
        seaborgium, bohrium, hassium, meitnerium, darmstadtium, roentgenium, copernicium, nihonium, flerovium, moscovium, livermorium, tennessium,
        oganesson, comment):
        return [OperationStateMapper.init_scalar(item) for item in mongo_mediator.select_operation_states(
            timestamp = parse_timestamp_parameter(timestamp),
            boat = parse_objectid_parameter(boat),
            operation = parse_objectid_parameter(operation),
            status = status, distance = distance, zenith = zenith, azimuth = azimuth, 
            hydrogenium = hydrogenium, helium = helium, lithium = lithium, beryllium = beryllium, borum = borum, carboneum = carboneum, 
            nitrogenium = nitrogenium, oxygenium = oxygenium, fluorum = fluorum, neon = neon, natrium = natrium, magnesium = magnesium, 
            aluminium = aluminium, silicium = silicium, phosphorus = phosphorus, sulfur = sulfur, chlorum = chlorum, argon = argon, kalium = kalium, 
            calcium = calcium, scandium = scandium, titanium = titanium, vanadium = vanadium, chromium = chromium, manganum = manganum, 
            ferrum = ferrum, cobaltum = cobaltum, niccolum = niccolum, cuprum = cuprum, zincum = zincum, gallium = gallium, germanium = germanium, 
            arsenicum = arsenicum, selenium = selenium, bromum = bromum, crypton = crypton, rubidium = rubidium, strontium = strontium, 
            yttrium = yttrium, zirconium = zirconium, niobium = niobium, molybdaenum = molybdaenum, technetium = technetium, ruthenium = ruthenium, 
            rhodium = rhodium, palladium = palladium, argentum = argentum, cadmium = cadmium, indium = indium, stannum = stannum, stibium = stibium, 
            tellurium = tellurium, iodium = iodium, xenon = xenon, caesium = caesium, barium = barium, lanthanum = lanthanum, cerium = cerium, 
            praseodymium = praseodymium, neodymium = neodymium, promethium = promethium, samarium = samarium, europium = europium, gadolinium = gadolinium, 
            terbium = terbium, dysprosium = dysprosium, holmium = holmium, erbium = erbium, thulium = thulium, ytterbium = ytterbium, lutetium = lutetium, 
            hafnium = hafnium, tantalum = tantalum, wolframium = wolframium, rhenium = rhenium, osmium = osmium, iridium = iridium, platinum = platinum, 
            aurum = aurum, hydrargyrum = hydrargyrum, thallium = thallium, plumbum = plumbum, bismuthum = bismuthum, polonium = polonium, astatum = astatum, 
            radon = radon, francium = francium, radium = radium, actinium = actinium, thorium = thorium, protactinium = protactinium, uranium = uranium, 
            neptunium = neptunium, plutonium = plutonium, americium = americium, curium = curium, berkelium = berkelium, californium = californium, 
            einsteinium = einsteinium, fermium = fermium, mendelevium = mendelevium, nobelium = nobelium, lawrencium = lawrencium, 
            rutherfordium = rutherfordium, dubnium = dubnium, seaborgium = seaborgium, bohrium = bohrium, hassium = hassium, meitnerium = meitnerium, 
            darmstadtium = darmstadtium, roentgenium = roentgenium, copernicium = copernicium, nihonium = nihonium, flerovium = flerovium, 
            moscovium = moscovium, livermorium = livermorium, tennessium = tennessium, oganesson = oganesson, comment = comment, ids = {'_id': id})]

    @staticmethod
    def init_scalar(item):
        return OperationStateMapper(id = str(item['_id']),
                               timestamp = stringify_timestamp_parameter(item['timestamp']),
                               boat = str(item['boat']),
                               operation = str(item['operation']),
                               status = item['status'],
                               distance = item['distance'],
                               zenith = item['zenith'],
                               azimuth = item['azimuth'],
                               comment = item['comment'],
                               hydrogenium = item['hydrogenium'],
                               helium = item['helium'],
                               lithium = item['lithium'],
                               beryllium = item['beryllium'],
                               borum = item['borum'],
                               carboneum = item['carboneum'],
                               nitrogenium = item['nitrogenium'],
                               oxygenium = item['oxygenium'],
                               fluorum = item['fluorum'],
                               neon = item['neon'],
                               natrium = item['natrium'],
                               magnesium = item['magnesium'],
                               aluminium = item['aluminium'],
                               silicium = item['silicium'],
                               phosphorus = item['phosphorus'],
                               sulfur = item['sulfur'],
                               chlorum = item['chlorum'],
                               argon = item['argon'],
                               kalium = item['kalium'],
                               calcium = item['calcium'],
                               scandium = item['scandium'],
                               titanium = item['titanium'],
                               vanadium = item['vanadium'],
                               chromium = item['chromium'],
                               manganum = item['manganum'],
                               ferrum = item['ferrum'],
                               cobaltum = item['cobaltum'],
                               niccolum = item['niccolum'],
                               cuprum = item['cuprum'],
                               zincum = item['zincum'],
                               gallium = item['gallium'],
                               germanium = item['germanium'],
                               arsenicum = item['arsenicum'],
                               selenium = item['selenium'],
                               bromum = item['bromum'],
                               crypton = item['crypton'],
                               rubidium = item['rubidium'],
                               strontium = item['strontium'],
                               yttrium = item['yttrium'],
                               zirconium = item['zirconium'],
                               niobium = item['niobium'],
                               molybdaenum = item['molybdaenum'],
                               technetium = item['technetium'],
                               ruthenium = item['ruthenium'],
                               rhodium = item['rhodium'],
                               palladium = item['palladium'],
                               argentum = item['argentum'],
                               cadmium = item['cadmium'],
                               indium = item['indium'],
                               stannum = item['stannum'],
                               stibium = item['stibium'],
                               tellurium = item['tellurium'],
                               iodium = item['iodium'],
                               xenon = item['xenon'],
                               caesium = item['caesium'],
                               barium = item['barium'],
                               lanthanum = item['lanthanum'],
                               cerium = item['cerium'],
                               praseodymium = item['praseodymium'],
                               neodymium = item['neodymium'],
                               promethium = item['promethium'],
                               samarium = item['samarium'],
                               europium = item['europium'],
                               gadolinium = item['gadolinium'],
                               terbium = item['terbium'],
                               dysprosium = item['dysprosium'],
                               holmium = item['holmium'],
                               erbium = item['erbium'],
                               thulium = item['thulium'],
                               ytterbium = item['ytterbium'],
                               lutetium = item['lutetium'],
                               hafnium = item['hafnium'],
                               tantalum = item['tantalum'],
                               wolframium = item['wolframium'],
                               rhenium = item['rhenium'],
                               osmium = item['osmium'],
                               iridium = item['iridium'],
                               platinum = item['platinum'],
                               aurum = item['aurum'],
                               hydrargyrum = item['hydrargyrum'],
                               thallium = item['thallium'],
                               plumbum = item['plumbum'],
                               bismuthum = item['bismuthum'],
                               polonium = item['polonium'],
                               astatum = item['astatum'],
                               radon = item['radon'],
                               francium = item['francium'],
                               radium = item['radium'],
                               actinium = item['actinium'],
                               thorium = item['thorium'],
                               protactinium = item['protactinium'],
                               uranium = item['uranium'],
                               neptunium = item['neptunium'],
                               plutonium = item['plutonium'],
                               americium = item['americium'],
                               curium = item['curium'],
                               berkelium = item['berkelium'],
                               californium = item['californium'],
                               einsteinium = item['einsteinium'],
                               fermium = item['fermium'],
                               mendelevium = item['mendelevium'],
                               nobelium = item['nobelium'],
                               lawrencium = item['lawrencium'],
                               rutherfordium = item['rutherfordium'],
                               dubnium = item['dubnium'],
                               seaborgium = item['seaborgium'],
                               bohrium = item['bohrium'],
                               hassium = item['hassium'],
                               meitnerium = item['meitnerium'],
                               darmstadtium = item['darmstadtium'],
                               roentgenium = item['roentgenium'],
                               copernicium = item['copernicium'],
                               nihonium = item['nihonium'],
                               flerovium = item['flerovium'],
                               moscovium = item['moscovium'],
                               livermorium = item['livermorium'],
                               tennessium = item['tennessium'],
                               oganesson = item['oganesson'])
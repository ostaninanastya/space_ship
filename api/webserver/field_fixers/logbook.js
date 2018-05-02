
function fix_fields(entity_name){
	if (entity_name == 'position'){
		return 'x, y, z'
	} else if (entity_name == 'controlaction'){
		return 'userid, command, params, result'
	} else if (entity_name == 'systemtest'){
		return 'system, result, date, time'
	}  else if (entity_name == 'operationstate'){
		return 'zenith, azimuth, date, time'
	}   else if (entity_name == 'shiftstate'){
		return 'date, time, remainingcartridges, remainingair, remainingelectricity, warninglevel'
	} else if (entity_name == 'sensordata'){
		return 'date, time, valuename, value, units'
	}
}

var entities = ['position', 'systemtest', 'operationstate', 'shiftstate', 'sensordata']

exports.fix_fields = fix_fields;
exports.entities = entities;
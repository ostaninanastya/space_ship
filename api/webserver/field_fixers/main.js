

// import


const logbook = require(process.env.SPACE_SHIP_HOME + '/api/webserver/field_fixers/logbook');


function fix_fields(entity_name){
	if (logbook.entities.includes(entity_name)) return logbook.fix_fields(entity_name);
}

exports.fix_fields = fix_fields;
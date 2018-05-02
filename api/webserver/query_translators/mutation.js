

// import


const fs = require("fs");

const yaml_js = require('yaml-js');

const fix_fields = require(process.env.SPACE_SHIP_HOME + '/api/webserver/field_fixers/main.js').fix_fields;
const string_operators = require(process.env.SPACE_SHIP_HOME + '/api/webserver/string_operators/main.js')

var split2 = string_operators.split2;
var capitalize = string_operators.capitalize


// set global variables


var REQUIREMENT_DELIMITER = '';

fs.readFile(process.env.SPACE_SHIP_HOME + '/api/webserver/config.yaml', 'utf8', function(err, contents) {
    var config = yaml_js.load(contents)

	REQUIREMENT_DELIMITER = config.requirement_delimiter;
});


function translate_mutation(query){
	let entity_name = query[3]
	let action_name = query[2]		
		
	let fields = ''
	let where = ''

	let requirements = (query[4] + query.slice(5).join('')).split('&')

	requirements.forEach(function(item){
		
		requirement = item.split(REQUIREMENT_DELIMITER);
		
		if (requirement[0] == 'fields'){
			fields = requirement[1]
		} else if (requirement[0] == 'where'){
			where = requirement[1]
		}
	});

	if (fields.length == 0) fields = fix_fields(entity_name);

	entity_name = capitalize(entity_name);

	if (where.length == 0){
		return ''
	} else {
		return `mutation Mutation{ ${action_name}${entity_name}(${where})`.replace(/\'/g, '"') + `{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}').replace(/\%20/g, ' ')
	}
}

exports.translate_mutation = translate_mutation;

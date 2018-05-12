

// import


const fs = require("fs");

const yaml_js = require('yaml-js');

const fix_fields = require(process.env.SPACE_SHIP_HOME + '/api/webserver/field_fixers/main.js').fix_fields;
const string_operators = require(process.env.SPACE_SHIP_HOME + '/api/webserver/string_operators/main.js')

var split2 = string_operators.split2;
var capitalize = string_operators.capitalize

const stringify_list_members = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/post_query_converters.js').stringify_list_members;
const object_to_list = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/post_query_converters.js').object_to_list;

// set global variables


var REQUIREMENT_DELIMITER = '';

fs.readFile(process.env.SPACE_SHIP_HOME + '/api/webserver/config.yaml', 'utf8', function(err, contents) {
    var config = yaml_js.load(contents)

	REQUIREMENT_DELIMITER = config.requirement_delimiter;
});

function get_graphql_mutation(fields, where, action_name, entity_name){
	if (fields.length == 0) fields = fix_fields(entity_name);

	entity_name = capitalize(entity_name);

	if (where.length == 0){
		return ''
	} else {
		return `mutation Mutation{ ${action_name}${entity_name}(${where})`.replace(/\'/g, '"') + `{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}').replace(/\%20/g, ' ')
	}
}


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

	return get_graphql_mutation(fields, where, action_name, entity_name);
}

function translate_post_mutation(query){
	let entity_name = query.entity;
	let action_name = query.operation;		
		
	let fields = stringify_list_members(query.fields).join(",");
	let where = object_to_list(query.where).join(",");

	return get_graphql_mutation(fields, where, action_name, entity_name);
}

exports.translate_post_mutation = translate_post_mutation;
exports.translate_mutation = translate_mutation;

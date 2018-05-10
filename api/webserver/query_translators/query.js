

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


function protect_commas(str){
	var inside = false;
	for (var i = 0; i < str.length; i++) { 
    	current = str.charAt(i);
    	if (current == '\''){
    		inside = !inside;
    	} else if ((current == ',') && inside){
    		str = str.substr(0, i) + '{{comma}}' + str.substr(i + 1);
    	}
    }
    return str; 	
}

function remake_commas(str){
    return str.replace(/\{\{comma\}\}/, ','); 	
}


function translate_query(query){
	
	let entity_name = query[2]

	let fields = ''
	let where = ''
	let set = ''

	let requirements = (query[3] + (query.length > 4 ? query.slice(3).join('/') : '')).split('&')

	requirements.forEach(function(item){

		requirement = item.split(REQUIREMENT_DELIMITER);
		if (requirement[0] == 'fields'){
			fields = requirement[1]
		} else if (requirement[0] == 'where'){
			where = requirement[1]
		} else if (requirement[0] == 'set'){
			set = requirement[1]
		}
	});

	console.log(fields);

	if (fields.length == 0) fields = fix_fields(entity_name);

	if ((where.length == 0) && (set.length == 0)){
		return `query Query{ ${entity_name}{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}')
	} else if (set.length == 0){
		return `query Query{ ${entity_name}(${where})`.replace(/\'/g, '"') + `{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}')
	} else {
		new_set = ''

		set = protect_commas(set);
			
		set.split(',').forEach(function(field){
			splitted_field = split2(field, ':')
			field_name = splitted_field[0]
			new_set += 'set' + field_name[0].toUpperCase() + field_name.substring(1,field_name.length).toLowerCase() + ':' + remake_commas(splitted_field[1]) + ','
		})

		entity_name = capitalize(entity_name);

		return `mutation Mutation{ update${entity_name}(${where}, ${new_set})`.replace(/\'/g, '"') + `{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}').replace(/\%20/g, ' ')
	}
}

exports.translate_query = translate_query;

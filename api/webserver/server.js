var express = require('express');
var spawn = require("child_process").spawn;
var app = express();

const PORT = 1881
const LAST_RESPONSE_CHUNK_SIGN = '====='

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

function translate_to_graphsql(original_query){
	
	let query = original_query.split('/')
	
	let entity_name = query[2]

	if (entity_name == 'create' || entity_name == 'remove' || entity_name == 'eradicate'){
		let action_name = entity_name
		entity_name = query[3]
		let requirements = query[4].split('&')

		let fields = ''
		let where = ''

		requirements.forEach(function(item){
			requirement = item.split('=');
			if (requirement[0] == 'fields'){
				fields = requirement[1]
			} else if (requirement[0] == 'where'){
				where = requirement[1]
			}
		});

		if (fields.length == 0){
			fields = fix_fields(entity_name)
		}

		entity_name = entity_name[0].toUpperCase() + entity_name.substring(1,entity_name.length).toLowerCase();

		if (where.length == 0){
			return ''
		} else {
			return `mutation Mutation{ ${action_name}${entity_name}(${where})`.replace(/\'/g, '"') + `{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}').replace(/\%20/g, ' ')
		}


	} else {
		let requirements = query[3].split('&')

		let fields = ''
		let where = ''

		requirements.forEach(function(item){
			requirement = item.split('=');
			if (requirement[0] == 'fields'){
				fields = requirement[1]
			} else if (requirement[0] == 'where'){
				where = requirement[1]
			}
		});

		if (fields.length == 0){
			fields = fix_fields(entity_name)
		}

		if (where.length == 0){
			return `query Query{ ${entity_name}{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}')
		} else {
			return `query Query{ ${entity_name}(${where})`.replace(/\'/g, '"') + `{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}')
		}
	}
}

app.listen(PORT, function () {
    console.log('The server is listening on port ' + PORT);
 });

app.get('/api/*', function(req, res){
	
	query = translate_to_graphsql(req.originalUrl).replace(/%20/g, ' ');

	console.log(query)

	let process = spawn('python3', ["../background/main.py", query]);

	res.write('<p style="white-space:pre;">')

	process.stdout.on('data', function(data){
		if (data.indexOf(LAST_RESPONSE_CHUNK_SIGN) == -1){
			res.write(data.toString('utf8'));
		} else {
			res.end(data.toString('utf8') + '</p>');
		}
		console.log(data.toString('utf8'));
	});

	process.stderr.on('data', function(data){
		console.log(data.toString('utf8'));
	});
});

app.get('/docs/', function(req, res){
	
	query = 'query Docs{__schema{types{name, fields{name, type{name, kind}}}}}';

	console.log(query)

	let process = spawn('python3', ["../background/main.py", query]);

	res.write('<p style="white-space:pre;">')

	result = ''

	res.write('=== Queries ===\n\n')

	res.write('= Entities =\n\n')

	process.stdout.on('data', function(data){
		if (data.indexOf(LAST_RESPONSE_CHUNK_SIGN) == -1){
			result += data.toString('utf8');
		} else {
			result += data.toString('utf8');
			parsed = JSON.parse(result.replace(LAST_RESPONSE_CHUNK_SIGN, ''))
			parsed['__schema']['types'].forEach(function(item){
				if (item['name'].includes('Mapper')){
					res.write('    ' + item['name'].toLowerCase().replace('mapper','') + '{\n')
					item['fields'].forEach(function(field){
						res.write('        ' + field['name'] + ': ' + (field['type']['name'] ? field['type']['name'] : 'List') + '\n');
					});
					res.write('    }\n\n');
				}
				
			});

			res.write('= Examples =\n\n')

			res.write('http://localhost:1881/api/shiftstate/fields=shiftid,time,shift(id,start,end,chief(id))&where=minute:42\n\n');
			
			let nested_process = spawn('python3', ["../background/main.py", 'docs']);

			result = ''

			res.write('=== Mutations ===\n\n')

			res.write('= Entities =\n\n')

			nested_process.stdout.on('data', function(data){
				if (data.indexOf(LAST_RESPONSE_CHUNK_SIGN) == -1){
					res.write(data.toString('utf8'));
				} else {
					res.write(data.toString('utf8'));
					res.write('= Examples =\n\n');
					res.write("http://localhost:1881/api/create/position/fields=ok,position(x)&where=timestamp:'2017-02-18 23:59:57',x:10.0,y:10.2,z:10.3,speed:10.4,attackangle:10.5,directionangle:10.6\n\n");
					res.end('</p>');
				}
				//console.log(data.toString('utf8'));
			});

			
		}
		//console.log(data.toString('utf8'));
	});

	process.stderr.on('data', function(data){
		console.log(data.toString('utf8'));
	});

	
});
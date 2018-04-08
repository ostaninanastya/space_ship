var express = require('express');
var spawn = require("child_process").spawn;
var app = express();

const PORT = 1881
const LAST_RESPONSE_CHUNK_SIGN = '====='

function fix_fields(entity_name){
	if (entity_name == 'position'){
		return 'x, y, z'
	} else if (entity_name == 'controlaction'){
		return 'username, command, params, result'
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
		return `query Query{ ${entity_name}(${where})` + `{ ${fields} }}`.replace(/\(/g, '{').replace(/\)/g, '}')
	}
}

app.listen(PORT, function () {
    console.log('The server is listening on port ' + PORT);
 });

app.get('/api/*', function(req, res){
	
	query = translate_to_graphsql(req.originalUrl);

	console.log(query)

	let process = spawn('python3', ["../background/test.py", query]);

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


// import


const spawn = require("child_process").spawn;
const fs = require("fs");

const yaml_js = require('yaml-js');


// set global variables


var LAST_RESPONSE_CHUNK_SIGN = '';

fs.readFile(process.env.SPACE_SHIP_HOME + '/api/webserver/config.yaml', 'utf8', function(err, contents) {
    var config = yaml_js.load(contents)

	LAST_RESPONSE_CHUNK_SIGN = config.last_response_chunk_sign;
});


function handle_docs_request(req, res){
	
	query = 'query Docs{__schema{types{name, fields{name, type{name, kind}}}}}';

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

}

exports.handle_docs_request = handle_docs_request;
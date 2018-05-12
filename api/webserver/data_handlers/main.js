

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

function send_response(layer, entity, res){

	if (!entity) entity = "";

	let python_process = spawn('python3', [process.env.SPACE_SHIP_HOME + "/transporters/show_layer_content.py", layer, entity]);

	res.write('')

	python_process.stdout.on('data', function(data){
		if (data.indexOf(LAST_RESPONSE_CHUNK_SIGN) == -1){
			res.write(data.toString('utf8'));
		} else {
			res.end(data.toString('utf8').replace(LAST_RESPONSE_CHUNK_SIGN, '') + '');
		}
		console.log(data.toString('utf8'));
	});

	python_process.stderr.on('data', function(data){
		console.log(data.toString('utf8'));
	});
}


function handle_data_request(req, res){
	send_response(req.body.layer, req.body.entity, res);
}

exports.handle_data_post_request = handle_data_request;
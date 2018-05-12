

// import


const fs = require('fs');

const express = require('express');
const yaml_js = require('yaml-js');

const handle_docs_request = require(process.env.SPACE_SHIP_HOME + '/api/webserver/docs_handlers/main.js').handle_docs_request;
const handle_api_request = require(process.env.SPACE_SHIP_HOME + '/api/webserver/api_handlers/main.js').handle_api_request;
const handle_api_post_request = require(process.env.SPACE_SHIP_HOME + '/api/webserver/api_handlers/main.js').handle_api_post_request;

const handle_data_post_request = require(process.env.SPACE_SHIP_HOME + '/api/webserver/data_handlers/main.js').handle_data_post_request;

const bodyParser = require('body-parser');

// set global variables


var PORT = 0;
var LAST_RESPONSE_CHUNK_SIGN = '';

fs.readFile(process.env.SPACE_SHIP_HOME + '/api/webserver/config.yaml', 'utf8', function(err, contents) {
    var config = yaml_js.load(contents)

    PORT = config.port;
	LAST_RESPONSE_CHUNK_SIGN = config.last_response_chunk_sign;

	start_server();
});


// start server

const app = express();
app.use(bodyParser.json());

function start_server(){
	app.listen(PORT, function () {
    	console.log('The server is listening on port ' + PORT);
 	});

	app.get('/api/*', function(req, res){
		handle_api_request(req, res);
	});

	app.post('/api/*', function(req, res){
		handle_api_post_request(req, res);
	});

	app.post('/data/*', function(req, res){
		handle_data_post_request(req, res);
	});

	app.get('/docs/', function(req, res){ 
		handle_docs_request(req, res); 
	});
}
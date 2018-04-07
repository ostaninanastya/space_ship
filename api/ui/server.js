var express = require('express');
var spawn = require("child_process").spawn;
var app = express();

const PORT = 1881

app.listen(PORT, function () {
    console.log('The server is listening on port ' + PORT);
 });

app.get('/api/*', function(req, res){
	arr = req.originalUrl.split('/')
	console.log(arr)

	if (arr.length == 4){
		if (arr[2] == 'position'){
			arr[4] = 'x, y, z'
		} else if (arr[2] == 'controlaction'){
			arr[4] = 'username, command, params, result'
		} else if (arr[2] == 'systemtest'){
			arr[4] = 'system, result, date, time'
		}
	} else if (arr.length == 3){
		arr[3] = ''
		if (arr[2] == 'position'){
			arr[4] = 'x, y, z'
		} else if (arr[2] == 'controlaction'){
			arr[4] = 'username, command, params, result'
		} else if (arr[2] == 'systemtest'){
			arr[4] = 'system, result, date, time'
		}
	} else if (arr.length < 3){
		console.log('too small')
		res.send('possible addresses are [positions]');
		return;
	}
	if (arr[3] != ''){
		arr[3] = '(' + arr[3] + ')'
	}
 	
	console.log('query Mine { ' + arr[2] + arr[3] + ' { ' + arr[4] + '}}');

	let process = spawn('python3', ["../background/test.py", 'query Mine { ' + arr[2] + arr[3] + ' { ' + arr[4] + '}}'], 
		{'SPACE_SHIP_HOME' : '/home/zeionara/Documents/space_ship'});

	process.stdout.on('data', function(data){
		console.log(data.toString('utf8'));
		res.send('<p style="white-space:pre;">' + data.toString('utf8') + '</p>');
	});

	process.stderr.on('data', function(data){
		console.log(data.toString('utf8'));
	});

    //res.send('all ok');
});
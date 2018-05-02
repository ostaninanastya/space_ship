

// import


const translate_mutation = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/mutation').translate_mutation;
const translate_query = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/query').translate_query;


// set global variables


var mutation_actions = ['create', 'remove', 'eradicate'];

function translate_to_graphsql(original_query){
	
	let query = original_query.replace(/%26/g, '&').replace(/%27/g, '\'').split('/')

	if (mutation_actions.includes(query[2])){
		return translate_mutation(query);
	} else {
		return translate_query(query);
	}
}

exports.translate = translate_to_graphsql;
exports.translate_mutation = translate_mutation;
exports.translate_query = translate_query;
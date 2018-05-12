

// import


const translate_mutation = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/mutation').translate_mutation;
const translate_query = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/query').translate_query;

const translate_post_mutation = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/mutation').translate_post_mutation;
const translate_post_query = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/query').translate_post_query;


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

function translate_to_graphsql_from_post(query){
	if (mutation_actions.includes(query.operation)){
		return translate_post_mutation(query);
	} else {
		return translate_post_query(query);
	}
}

exports.translate = translate_to_graphsql;
exports.translate_post = translate_to_graphsql_from_post;
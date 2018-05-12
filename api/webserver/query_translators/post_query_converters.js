function stringify_list_members(src_list){
	console.log(src_list);
	let dst_list = [];
	src_list.forEach(function(item){
		if ((typeof item) == "string"){
			dst_list.push(item);
		} else {
			console.log(Object.keys(item)[0]);
			console.log('bef ', dst_list);
			dst_list.push(`${Object.keys(item)[0]}(${stringify_list_members(item[Object.keys(item)[0]]).join(',')})`)
			console.log('aft ', dst_list);
		}
		console.log(dst_list);
	});
	return dst_list;
}

function object_to_list(obj){
	list = [];
	if (obj){
		Object.keys(obj).forEach(function(key) {
			if ((typeof obj[key]) == "string"){
				list.push(`${key}:'${obj[key]}'`);
			} else {
				list.push(`${key}:${obj[key]}`);
			}
		});
	}
	return list;
}

exports.stringify_list_members = stringify_list_members;
exports.object_to_list = object_to_list;
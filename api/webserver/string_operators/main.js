
function split2(str, delim){
    var p=str.indexOf(delim);
    if (p !== -1) {
        return [str.substring(0,p), str.substring(p+1)];
    } else {
        return [str];
    }
}

function capitalize(str){
	return str[0].toUpperCase() + str.substring(1, str.length).toLowerCase();
}

exports.split2 = split2;
exports.capitalize = capitalize;
var result = ''

document.getElementsByClassName('wikitable sortable jquery-tablesorter')[0].childNodes[2].childNodes.forEach(function callback(item){
	if(item.childNodes[3]){
		result += ', ' + item.childNodes[7].childNodes[0].data
	}
    
});

console.log(result)
var result = ''

i = 7

document.getElementsByClassName('wikitable sortable jquery-tablesorter')[0].childNodes[2].childNodes.forEach(function callback(item){
	if(item.childNodes[3]){
		if (item.childNodes[7].childNodes[0].data){
			result += item.childNodes[7].childNodes[0].data.toLowerCase() + ` = item[${i}], `
			i += 1
		}
	}
    
});

console.log(result)

var HOST = 'http://' + ADDRESS + ':' + PORT;

String.prototype.hashCode = function(){
	    var hash = 0;
	    if (this.length == 0) return hash;
	for (i = 0; i < this.length; i++) {
		char = this.charCodeAt(i);
		hash = ((hash<<5)-hash)+char;
		hash = hash & hash; // Convert to 32bit integer
	}
	return hash;
}

function scroll(elem_id) {
    var elmnt = document.getElementById(elem_id);
    elmnt.scrollIntoView();
}

function parse(text){
    var pattern = new RegExp("(http(s)?:\/\/[^ \n]+)", 'ig');
    return text
        .replace(pattern, '<a href="$1" target="_blank">$1</a>')
        .replace(/\n/g, '<br />');
}

function get(params, callback){
    $.get(HOST + params).then(function(data){
        callback(data);
    });
}

function post(data, callback){
    $.post(HOST, data).then(function(res){
        callback(res);
    });
}

function parse_tags(tags){
    var parsed_tags = [];
    var pieces = tags.split(',');
    for (var i = 0; i < pieces.length; i++){
        parsed_tags.push(pieces[i].trim());
    }
    return parsed_tags;
}

function add(){
    var key = $('#key').val();
    var val = $('#val').val();
    var tags = $('#tags').val();
    var localstorage = $('#localstorage').prop('checked');
    if (key.length > 0 && val.length > 0)
        if (localstorage)
            add_to_localstorage(key, val, tags);
        else
            add_to_db(key, val, tags);
}

function add_to_db(key, val, tags){
  	get('?exists=1&key=' + key, function(exists){
        if (exists){
  	        var r = confirm(key + " already exist. Do you want to replace it?");
		    if (r === false) return;
        }
        get('?add=1&key=' + key + '&val=' + val + '&tags=' + tags, function(data){
            clear();
            refresh();
        });
    });
}

function add_to_localstorage(key, val, tags){
    var tags = parse_tags($('#tags').val());
    if (localStorage.getItem(key)){
        var r = confirm(key + " already exist. Do you want to replace it?");
        if (r === false) return;
    }
    var values = JSON.stringify({
        'val': val,
        'tags': tags
    });
    localStorage.setItem(key, values);
    clear();
    refresh();
}

function get_item_from_localstorage(index){
    var key = localStorage.key(index);
    var values = JSON.parse(localStorage.getItem(key));
    return {
        key: key,
        val: values['val'],
        tags: values['tags']
    }
}


function edit(index) {
    var pieces = index.split('_');
    if (pieces.length == 2){
        index = pieces[2];
        var item = get_item_from_localstorage(index);
  	    $('#key').val(item['key']);
	    $('#val').val(item['val']);
	    $('#tags').val(item['tags']);
	    $('#localstorage').attr("checked", true);
  	    window.scrollTo(0, 0);
    } else {
        get('?getitem=1&index=' + index, function(data){
  	        $('#key').val(data['key']);
	        $('#val').val(data['val']);
	        $('#tags').val(data['tags']);
	        $('#localstorage').attr("checked", false);
  	        window.scrollTo(0, 0);
  	    });
    }
}

function del(index) {
    var r = confirm("Are you sure you want to remove it?");
	if (r === true) {
	    var pieces = index.split('_');
        if (pieces.length == 2){
            index = pieces[2];
            localStorage.removeItem(localStorage.key(index));
  	        refresh();
        } else {
	        get('?del=1&index=' + index, function(data){
  	            refresh();
  	        });
  	    }
	}
}



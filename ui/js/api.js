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
            add_to_localstorage(key, val, tags, CURRENT_TAB);
        else
            add_to_db(key, val, tags, CURRENT_TAB);
}

function add_to_db(key, val, tags, tab){
  	post('/exists', {key: key, tab: tab}, function(exists){
        if (exists){
  	        var r = confirm(key + " already exist. Do you want to replace it?");
		    if (r === false) return;
        }
        data = {
            key: key,
            val: val,
            tags: tags,
            tab: tab
        }
        console.log('here');
        post('/add', data, function(res){
            clear();
            refresh();
        });
    });
}

function add_to_localstorage(key, val, tags, tab){
    var tags = parse_tags($('#tags').val());
    if (localStorage.getItem(key)){
        var r = confirm(key + " already exist. Do you want to replace it?");
        if (r === false) return;
    }
    var values = JSON.stringify({
        'val': val,
        'tags': tags,
        'tab': tab
    });
    localStorage.setItem(key, values);
    clear();
    refresh();
}

function get_item_from_localstorage(index){
    var key = localStorage.key(index);
    var values = JSON.parse(localStorage.getItem(key));
    if ('val' in values && 'tags' in values && 'tab' in values)
        return {
            key: key,
            val: values['val'],
            tags: values['tags'],
            tab: values['tab']
        }
    else
        return null;
}


function edit(index) {
    var pieces = index.split('_');
    if (pieces.length == 2){
        index = pieces[1];
        var item = get_item_from_localstorage(index);
  	    $('#key').val(item['key']);
	    $('#val').val(item['val']);
	    $('#tags').val(item['tags']);
	    $('#localstorage').attr("checked", true);
  	    window.scrollTo(0, 0);
    } else {
        get('/getitem?index=' + index, function(data){
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
            index = pieces[1];
            localStorage.removeItem(localStorage.key(index));
  	        refresh();
        } else {
	        get('/delete?index=' + index, function(data){
  	            refresh();
  	        });
  	    }
	}
}

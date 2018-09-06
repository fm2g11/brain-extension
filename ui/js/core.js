
var colors = d3.scaleOrdinal(d3.schemeCategory10);
var converter = new showdown.Converter();

function add(){
    var key = $('#key').val();
    var val = $('#val').val();
    var tags = $('#tags').val();
    if (key.length > 0 && val.length > 0){
  		get('?exists=1&key=' + key, function(exists){
            if (exists){
  		        var r = confirm(key + " already exist. Do you want to replace it?");
		        if (r === false) return;
            }
            get('?add=1&key=' + key + '&val=' + val + '&tags=' + tags, function(data){
	  	        $('#key').val('');
	  	        $('#val').val('');
	  	        $('#tags').val('');
	  	        refresh();
            });
        });
  	}
};

function gen_tags(tags){
    var html = '';
  	for (var i = 0; i < tags.length; i++){
  	    var name = tags[i]
  	    html += tag_template({
  	        name: name,
  	        color: colors(name)
  	    })
    }
    return html
}

function refresh(){
   function _refresh(data){
        console.log(data)
        var html = '';

  	    for (var i = 0; i < data.length; i++){
  	        var item = data[i];
  	        var tags = gen_tags(item['tags']);
  	        html += item_template({
		        key: converter.makeHtml(item['key']),
		  	    val: converter.makeHtml(parse(item['val'])),
		  	    index: i,
		  	    tags: tags,
		  	    hash: item['key'].hashCode()
		    });
	    }
	    $('#items').html(html);
   };
   get('?get=1', _refresh);
};

function edit(index) {
    get('?getitem=1&index=' + index, function(data){
  	    $('#key').val(data['key']);
	    $('#val').val(data['val']);
	    $('#tags').val(data['tags']);
  	    window.scrollTo(0, 0);
  	});
};

function del(index) {
    var r = confirm("Are you sure you want to remove it?");
	if (r === true) {
	    get('?del=1&index=' + index, function(data){
  	        refresh()
  	    });

	}
};


$(document).ready(function(){
    refresh();
    $('#add').click(add);
//    var simplemde = new SimpleMDE({ element: $("#val")[0] });

});


var colors = d3.scaleOrdinal(d3.schemeCategory10);
var converter = new showdown.Converter();

function clear(){
    $('#key').val('');
	$('#val').val('');
	$('#tags').val('');
}

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

function make_table(data, localstorage){
    var html = '';
    var is_local = localstorage == 'checked' ? 'local_' : '';
    for (var i = 0; i < data.length; i++){
        var item = data[i];
        var tags = gen_tags(item['tags']);
        html += item_template({
            key: converter.makeHtml(item['key']),
            val: converter.makeHtml(parse(item['val'])),
            index: is_local + i,
            tags: tags,
            hash: item['key'].hashCode(),
            localstorage: localstorage
        });
    }
    return html
}
function get_local_data(){
    var local_data = [];
    for (var i = 0; i < localStorage.length; i++){
        var item = get_item_from_localstorage(i);
        local_data.push(item);
    }
    return local_data;
}

function refresh(){
   function _refresh(data){
        var html = make_table(data, "unchecked");
        var local_data = get_local_data()
        html += make_table(local_data, "checked");

	    $('#items').html(html);
	    $('#stats').html(data.length + local_data.length + ' items. ');
   };
   get('/get?', _refresh);
};

$(document).ready(function(){
    refresh();
    $('#add').click(add);
//    var simplemde = new SimpleMDE({ element: $("#val")[0] });
    var title = window.location.href.split('/')[2]
    $(document).attr("title", 'brain-extension (' + title);

});

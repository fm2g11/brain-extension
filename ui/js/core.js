var TABS = ['knowledge', 'thoughts']

var loc = window.location.href.split('/')[3]
var CURRENT_TAB = TABS.includes(loc) ? loc : 'knowledge';

var colors = d3.scaleOrdinal(d3.schemeCategory10);
var converter = new showdown.Converter();

function clear(){
    $('#key').val('');
	$('#val').val('');
	$('#tags').val('');
	$('#localstorage').attr("checked", false);
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
        var tab = item['tab'];
        if (tab != CURRENT_TAB) continue;
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
function get_local_items(){
    var local_items = [];
    for (var i = 0; i < localStorage.length; i++){
        var item = get_item_from_localstorage(i);
        local_items.push(item);
    }
    return local_items;
}

function tab_filter(item){
    return item['tab'] == CURRENT_TAB;
}

function stats(data, local_items){
    return stats_template({
        items: data['items'].filter(tab_filter).length + local_items.filter(tab_filter).length,
        tags: data['tags'].length,
    })
}

function refresh(){
   function _refresh(data){
        var items = data['items'];
        var tags = data['tags'];
        var html = make_table(items, "unchecked");
        var local_items = get_local_items()
        html += make_table(local_items, "checked");

	    $('#items').html(html);
	    $('#stats').html(stats(data, local_items));
   };
   get('/get?', _refresh);
};

function knowledge_tab(){
    CURRENT_TAB = 'knowledge';
    window.location.href = CURRENT_TAB;
}
function thoughts_tab(){
    CURRENT_TAB = 'thoughts';
    window.location.href = CURRENT_TAB;
}

function set_active_tab(){
    $('.nav-item').each(function(){
        $(this).removeClass('active');
    });
    $('#' + CURRENT_TAB + '-nav').attr('class', 'active');
}


$(document).ready(function(){
    $('#add_inputs').html(add_template());
    $('#table').html(table_template());
    refresh();
    $('#add').click(add);
    $('#knowledge-nav').click(knowledge_tab);
    $('#thoughts-nav').click(thoughts_tab);
    set_active_tab();

    var title = window.location.href.split('/')[2];
    $(document).attr("title", 'brain-extension (' + title + ')');
});

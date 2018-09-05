var HOST = 'http://localhost:8888/';

var item = _.template(`
    <tr>
        <th><%= key %></th>
        <td><%= val %></td>
        <td class="right-align">
            <button class="btn btn-warning" onclick="edit(<%= index %>)">
                <span class="glyphicon glyphicon-pencil"></span>
            </button>
        </td>
        <td class="right-align" onclick="del(<%= index %>)">
            <button class="btn btn-danger">
                <span class="glyphicon glyphicon-remove"></span>
            </button>
        </td>
    </tr>
`);

function get(params, callback){
    $.get(HOST + params).then(function(data){
        callback(data);
    });
}


function add(){
    var key = $('#key').val();
    var val = $('#val').val();
    if (key.length > 0 && val.length > 0){
  		get('?exists=1&key=' + key, function(exists){
            if (exists){
  		        var r = confirm(key + " already exist. Do you want to replace it?");
		        if (r === false) return;
            }
            get('?add=1&key=' + key + '&val=' + val, function(data){
	  	        $('#key').val('');
	  	        $('#val').val('');
  	            refresh();
            });
        });
  	}
};


function refresh(){
   function _refresh(data){
        console.log(data)
        var html = '';

  	    for (var i = 0; i < data.length; i++){
  	        html += item({
		        key: data[i][0],
		  	    val: data[i][1],
		  	    index: i
		    });
	    }
	    $('#items').html(html);
   };
   get('?get=1', _refresh);
};

function edit(index) {
    get('?getpair=1&index=' + index, function(data){
  	    $('#key').val(data['key']);
	    $('#val').val(data['val']);
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

//function can_add(){
//    var key = $('#key').val();
//    var val = $('#val').val();
//  	return (key.length > 0 && val.length > 0);
//};
//
//function is_disabled(){
//    return can_add() ? '' : 'disabled';
//}

$(document).ready(function(){
    refresh();
    $('#add').click(add);
});
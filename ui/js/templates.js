
var item_template = _.template(`
    <tr id="<%= hash %>">
        <td><%= tags %></td>
        <th><%= key %></th>
        <td><%= val %></td>
        <td><input type="checkbox" <%= localstorage %> disabled /></td>
        <td class="right-align">
            <button class="btn btn-warning" onclick="edit('<%= index %>')">
                <span class="glyphicon glyphicon-pencil"></span>
            </button>
        </td>
        <td class="right-align" onclick="del('<%= index %>')">
            <button class="btn btn-danger">
                <span class="glyphicon glyphicon-remove"></span>
            </button>
        </td>
    </tr>
`);

var tag_template = _.template(`
    <a class="d-inline-block IssueLabel v-align-text-top"
        style="background-color: <%= color %>; color: white"
        title="<%= name %>" href="">
        <%= name %>
    </a>
`);

var stats_template = _.template(`
    <p class="stats"><%= items %> items. <%= tags %> tags</p>
`);

var add_template = _.template(`
<div class="row">
    <div class="col-sm-3">
        <textarea class="form-control" rows="4" placeholder="Key" id="key"></textarea>
    </div>
    <div class="col-sm-5">
        <textarea class="form-control" rows="4" placeholder="Value" id="val"></textarea>
    </div>
    <div class="col-sm-2">
        <textarea class="form-control" rows="4" placeholder="Tags" id="tags"></textarea>
        <label for="localstorage">
            <input type="checkbox" id="localstorage" /> Store Locally
        </label>
    </div>


    <div class="col-sm-2">
        <button class="btn btn-success button" style="height:90px" id="add">Add</button>
    </div>
</div>
`);

var table_template = _.template(`
<div class="row">
    <div class="col-xs-12">
        <table class="table table-striped table-condensed">
            <thead>
                <tr>
                    <th>Tags</th>
                    <th class="key-column">Key</th>
                    <th>Value</th>
                    <th></th>
                    <th></th>
                </tr>
            </thead>
            <tbody id="items">
            </tbody>
        </table>
    </div>
</div>
<div class="row">
   <div id="stats" class="col-xs-12"></div>
</div>
`);

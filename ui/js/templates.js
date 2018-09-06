
var item_template = _.template(`
    <tr id="<%= hash %>">
        <td><%= tags %></td>
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

var tag_template = _.template(`
    <a class="d-inline-block IssueLabel v-align-text-top"
        style="background-color: <%= color %>; color: white"
        title="<%= name %>" href="">
        <%= name %>
    </a>
`);


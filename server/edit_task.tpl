%#template for editing a task
%#the template expects to receive a value for "id" as well a "old", the text of the selected ToDo item
%#  id is a str(ObjectId)
%#  old is a list: ['task', 'status']
<p>Edit the task with ID = {{id}}</p>
<form action="/edit/{{id}}" method="get">
  <input type="text" name="task" value="{{old}}" size="80" maxlength="80">
  <select name="status">
    <option>open</option>
    <option>closed</option>
  </select>
  <br>
  <input type="submit" name="save" value="save">
</form>
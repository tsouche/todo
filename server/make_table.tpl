%# template to generate a HTML table from a list of tuples (or list of lists, or 
%# tuple of tuples or ...)
%#
<p>The open items are as follows:</p>
<table border="1">
%for task in rows:
  <tr>
  %for item in task:
    <td>{{item}}</td>
  %end
  </tr>
%end
</table>
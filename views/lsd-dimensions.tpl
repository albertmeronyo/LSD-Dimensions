% include('header.tpl', title='CEDAR Harmonize')

<p>The following shows a list of the current dimensions (and their codes) in Linked Statistical Data. Lorem ipsum bla bla bla.</p>

<center>
<table class="table table-hover tablee-condensed">
  <tr><td class="ui-helper-center"><b>Dimension URI</b></td><td class="ui-helper-center"><b>Description</b></td></tr>
  %for result in results["result"]:
  %   dimension = result["_id"]["uri"]
  %   label = result["_id"]["label"]
  <tr>
    <td>
      <form name="edit{{dimension}}" action="/dimension" method="post">
	<input type="hidden" name="dim" value="{{dimension}}">
      <a href="javascript:document.forms['edit{{dimension}}'].submit();">{{dimension}}</a>
      </form>
    </td>
    <td>
      {{label}}
    </td>
  </tr>
  %end
</table>
</center>

<div class="row">
<a href="/harmonize/vocab/alldetails">
  <button type="button" class="btn btn-primary btn-md">View All Details</button>
</a>
</div>
<br>
<div class="row">
<a href="/harmonize">Back</a>
</div>

% include('footer.tpl')

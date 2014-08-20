% include('header.tpl', title='CEDAR Harmonize')

<h2>Harmonization vocabulary</h2>

<h3>Details for dimension {{dim}}</h3>
<br>
<p>Displaying the list of codes assigned to dimension {{dim}}</p>
<br>
<center>
<table class="table table-hover tablee-condensed">
  <tr><td class="ui-helper-center"><b>Code</b></td><td class="ui-helper-center"><b>Description</b></td></tr>
  %for detail in details["results"]["bindings"]:
  %   code = detail["code"]["value"] if "code" in detail else ""
  %   codel = detail["codel"]["value"] if "codel" in detail else ""
  %   codelist = detail["codelist"]["value"] if "codelist" in detail else ""
  %   concept = detail["concept"]["value"]
  <tr>
    <td>
      {{code}}
    </td>
    <td>
      {{codel}}
    </td>
  </tr>
  %end
</table>
</center>
<p>New codes can be added filling the form below. If a code list currently exists for this dimension, then that code list's URI will display on the first input field (multiple code lists for one dimension are currently not supported). Please fill in a code URI, a description of what it represents, and click Add Code.</p>
<br>
<form class="form-horizontal" role="form" method="post" action="/harmonize/vocab/addcode">
<div class="row">
  <div class="form-group">
    <input type="text" name="codelist" class="form-control" placeholder="Code list URI" {{"value=" + codelist if codelist else ""}}>
  </div>
  <div class="form-group">
    <input type="text" name="code" class="form-control" placeholder="Code URI">
  </div>
  <div class="form-group">
    <input type="text" name="codel" class="form-control" placeholder="Code description">
  </div>
  <input type="hidden" name="dim" value="{{dim}}">
  <input type="hidden" name="concept" value="{{concept}}">
  <div class="form-group">
    <a href="/harmonize/vocab/addcode">
      <input type="submit" class="btn btn-primary btn-md" value="Add Code">
    </a>
  </div>
</div>
</form>
<br><br>
<a href="/harmonize/vocab">Back</a>



% include('footer.tpl')

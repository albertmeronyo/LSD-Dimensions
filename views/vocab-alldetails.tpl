% include('header.tpl', title='CEDAR Harmonize')

<h2>Harmonization vocabulary</h2>

<h3>Showing all details for all dimensions</h3>

<p>This page displays all the details (concept, range, code list, and code) for all the dimensions in the harmonization vocabulary.</p>

<center>
<table class="table table-hover tablee-condensed">
  <tr><td class="ui-helper-center"><b>Dimension</b></td><td class="ui-helper-center"><b>Concept</b></td><td class="ui-helper-center"><b>Range</b></td><td class="ui-helper-center"><b>Code List</b></td><td class="ui-helper-center"><b>Code</b></td></tr>
  %for detail in details["results"]["bindings"]:
  %   dimension = detail["dimension"]["value"]
  %   concept = detail["concept"]["value"]
  %   range = detail["range"]["value"]
  %   codelist = detail["codelist"]["value"] if "codelist" in detail else ""
  %   code = detail["code"]["value"] if "code" in detail else ""
  <tr>
    <td>
      {{dimension}}
    </td>
    <td>
      {{concept}}
    </td>
    <td>
      {{range}}
    </td>
    <td>
      {{codelist}}
    </td>
    <td>
      {{code}}
    </td>
  </tr>
  %end
</table>
</center>
<br>
<a href="/harmonize/vocab">Back</a>


% include('footer.tpl')

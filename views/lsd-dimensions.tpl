% include('header.tpl', title='CEDAR Harmonize')

<div class="container" style="margin: 20px auto;">
<p>The following shows a list of the current dimensions (and their codes) in Linked Statistical Data. Lorem ipsum bla bla bla.</p>
%  num_dimensions = len(results["result"])
<p style="margin-bottom: 50px">We currently have <b>{{num_dimensions}}</b> dimensions in Linked Statistical Data. </p>


<table class="table table-hover table-condensed table-striped" style="width: 100%; white-space: nowrap; table-layout: fixed; text-align: left">
  <tr><td class="ui-helper-center" style="background-color: #222; color: #aaa;">Dimension URI</td><td class="ui-helper-center" style="background-color: #222; color: #aaa;">Label</td><td class="ui-helper-center" style="background-color: #222; color: #aaa;">References</td></tr>
  %for result in results["result"]:
  %   dimension = result["_id"]["uri"]
  %   label = result["_id"]["label"]
  %   refs = result["dimensionsCount"]
  <tr>
    <td style="overflow: hidden; text-overflow: ellipsis;">
      <a href="{{dimension}}" target="_blank">{{dimension}}</a>
    </td>
    <td style="overflow: hidden; text-overflow: ellipsis; text-align: center;">
      {{label}}
    </td>
    <td style="overflow: hidden; text-overflow: ellipsis; text-align: center;">
      {{refs}}
    </td>
  </tr>
  %end
</table>
</div>


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

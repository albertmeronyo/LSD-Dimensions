% include('header.tpl', title='CEDAR Harmonize')

<div class="container" style="margin: 20px auto;">
<p>The following shows a list of the current dimensions (and their codes) in Linked Statistical Data. Lorem ipsum bla bla bla.</p>
%  num_dimensions = len(results["result"])
<p style="margin-bottom: 50px">We currently have <b>{{num_dimensions}}</b> dimensions in Linked Statistical Data. </p>


<table id="lsd-dimensions" class="table table-hover table-condensed table-striped" style="width: 100%; white-space: nowrap; table-layout: fixed; text-align: left" data-toggle="table" data-url="data.json" data-sort-name="refs" data-sort-order="desc" data-pagination="true">
  <thead>
  <tr>
    <th data-field="uri" data-sortable="true" class="ui-helper-center" style="background-color: #222; color: #aaa;" >Dimension URI</th>
    <th data-field="label" data-sortable="true" class="ui-helper-center" style="background-color: #222; color: #aaa;">Label</th>
    <th data-field="refs" data-sortable="true" class="ui-helper-center" style="background-color: #222; color: #aaa;">References</th>
  </tr>
  </thead>
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

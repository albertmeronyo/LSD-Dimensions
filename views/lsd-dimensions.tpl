% include('header.tpl', page='home')

<div class="container" style="margin: 20px auto;">
%  num_dimensions = len(results["result"])
<p class="lead" style="margin-bottom: 50px">Counting <b>{{num_dimensions}}</b> dimensions in <b>{{num_endpoints}}</b> SPARQL endpoints in Linked Statistical Data</p>


<table id="lsd-dimensions" style="width: 100%; white-space: nowrap; table-layout: fixed; text-align: left" data-toggle="table" data-url="data.json" data-sort-name="refs" data-sort-order="desc" data-pagination="true" data-search="true" data-classes="table table-hover table-condensed table-striped" data-page-size="10">
  <thead>
  <tr>
    <th data-field="view" class="col-md-1"></th>
    <th data-field="uri" data-sortable="true" class="ui-helper-center">Dimension URI</th>
    <th data-field="label" data-sortable="true" class="ui-helper-center">Label</th>
    <th data-field="refs" data-sortable="true" class="ui-helper-center col-md-2">References</th>
  </tr>
  </thead>
</table>

</div>

% include('footer.tpl')

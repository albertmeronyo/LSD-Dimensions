% include('header.tpl', page='dsds')

% dsd_uri = dsd_results
<h2>Details for Data Structure Definition <a href="{{dsd_uri}}" target="_blank">{{dsd_uri}}</a></h2>

<div class="container">

<table class="table table-hover">

<tr>
  <td>Component</td>
  <td>Property</td>
  <td>Value</td>
</tr>
% for prop in dsd_results:
%   component = prop["dsd"]["components"]["s"]
%   property = prop["dsd"]["components"]["p"]
%   value = prop["dsd"]["components"]["o"]
<tr>
  <td>{{component}}</td>
  <td>{{property}}</td>
  <td>{{value}}</td>
</tr>
% end
</table>

</div>

<a href="/dsds">Back</a>

% include('footer.tpl')

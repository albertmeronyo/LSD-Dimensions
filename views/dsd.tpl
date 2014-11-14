% include('header.tpl', page='dsds')

% dsd_uri = dsd_results["dsd"]["uri"]
<h2>Details for Data Structure Definition <a href="{{dsd_uri}}" target="_blank">{{dsd_uri}}</a></h2>

<div class="container">

<table class="table table-hover tabe-condensed">

<tr>
  <td class="text-left">Component</td>
  <td class="text-left">Property</td>
  <td class="text-left">Value</td>
</tr>
% for prop in dsd_results["dsd"]["components"]:
%   component = prop["s"]
%   property = prop["p"]
%   value = prop["o"]
<tr>
  <td class="text-left">{{component}}</td>
  <td class="text-left">{{property}}</td>
  <td class="text-left">{{value}}</td>
</tr>
% end
</table>

</div>

<a href="/dsds">Back</a>

% include('footer.tpl')

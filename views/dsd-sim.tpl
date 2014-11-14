% include('header.tpl', page='dsds')

% dsd_uri = dsd_results["dsd"]["uri"]
<h2>Distances between all DSDs permutations</a></h2>

<div class="container">

<table class="table table-hover tabe-condensed">

<tr>
  <td>Component A</td>
  <td>Component B</td>
  <td>Distance</td>
</tr>
% for key, value in dist.iteritems():
%   component_a = key[0]
%   component_b = key[1]
%   distance = value
<tr>
  <td>{{component_a}}</td>
  <td>{{component_b}}</td>
  <td>{{distance}}</td>
</tr>
% end
</table>

</div>

<a href="/dsds">Back</a>

% include('footer.tpl')

% include('header.tpl', page='dsds')

<h2>Distances between all DSDs permutations (omitting 1.0)</a></h2>

<div class="container">

<table class="table table-hover tabe-condensed">

<tr>
  <td>DSD A</td>
  <td>DSD B</td>
  <td>Distance</td>
</tr>
% for key, value in dist.iteritems():
%   dsd_a_id = key[0]
%   dsd_b_id = key[1]
%   dsd_a_uri = dsd_uris[dsd_a_id]
%   dsd_b_uri = dsd_uris[dsd_b_id]
%   distance = value
%   if distance < 1.0 :
<tr>
  <td><a href="/dsds/{{dsd_a_id}}" target="_blank">{{dsd_a_uri}}</a></td>
  <td><a href="/dsds/{{dsd_b_id}}" target="_blank">{{dsd_b_uri}}</a></td>
  <td>{{distance}}</td>
</tr>
%   end
% end
</table>

</div>

<a href="/dsds">Back</a>

% include('footer.tpl')

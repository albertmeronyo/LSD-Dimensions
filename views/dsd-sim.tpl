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
%   dsd_a = key[0]
%   dsd_b = key[1]
%   distance = value
%   if distance < 1.0 :
<tr>
  <td><a href="{{dsd_a}}" target="_blank">{{dsd_a}}</a></td>
  <td><a href="{{dsd_b}}" target="_blank">{{dsd_b}}</a></td>
  <td>{{distance}}</td>
</tr>
%   end
% end
</table>

</div>

<a href="/dsds">Back</a>

% include('footer.tpl')

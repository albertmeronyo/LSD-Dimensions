% include('header.tpl', page='dsds')

<div class="container" style="margin: 20px auto;">
<p class="lead" style="margin-bottom: 50px">Counting <b>{{num_dsds}}</b> Data Structure Definitions in <b>{{num_endpoints}}</b> SPARQL endpoints in Linked Statistical Data</p>

<div class="container">
<dl class="dl-horizontal">
	<dt>Data Structure Definitions (DSDs)</dt>
	% for dsd in results:
	% 	dsd_uri = dsd["dsd"]["uri"]
	%	dsd_id = dsd["id"]
	<dd><a href="{{dsd_id}}">{{dsd_uri}}</a></dd>
	% end
</dl>
</div>

</div>

% include('footer.tpl')

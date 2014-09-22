% include('header.tpl', page='analytics')

<div class="container" style="margin: 20px auto;">

<h2>Analytics</h2>


<div class="row">
  <div class="col-md-6">
    <h3>Dimension frequency distribution</h3>
    <p class="text-justify">Distribution of distinct LSD dimensions according to the frequency in which they appear in LOD datasets.</p>
    <img src="img/dim-freq.png" class="img-responsive img-rounded">
  </div>
  <div class="col-md-6">
    <h3>Datasets using qb:DimensionProperty</h3>
    <p class="text-justify">Proportion of LOD datasets using any qb:DimensionProperty.</p>
    <img src="img/endpoint-usage.png" class="img-responsive img-rounded">
  </div> 
</div>

</div>

% include('footer.tpl')

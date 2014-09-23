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

<div class="row">
  <div class="col-md-6">
    <h3>Chart.js</h3>
    <p class="text-justify">foo bar foobar baz.</p>
    <canvas id="myChart" width="400" height="400"></canvas>
    <script>
      var ctx = document.getElementById("myChart").getContext("2d");
      var myNewChart = new Chart(ctx);
      var data = {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
      {
      label: "My First dataset",
      fillColor: "rgba(220,220,220,0.2)",
      strokeColor: "rgba(220,220,220,1)",
      pointColor: "rgba(220,220,220,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(220,220,220,1)",
      data: [65, 59, 80, 81, 56, 55, 40]
      },
      {
      label: "My Second dataset",
      fillColor: "rgba(151,187,205,0.2)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(151,187,205,1)",
      data: [28, 48, 40, 19, 86, 27, 90]
      }
      ]
      };
      var myLineChart = new Chart(ctx).Line(data, options);
    </script>
  </div>
  <div class="col-md-6">
    <h3>Datasets using qb:DimensionProperty</h3>
    <p class="text-justify">Proportion of LOD datasets using any qb:DimensionProperty.</p>
    <img src="img/endpoint-usage.png" class="img-responsive img-rounded">
  </div> 
</div>


</div>

% include('footer.tpl')

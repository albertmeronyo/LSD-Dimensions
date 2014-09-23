% include('header.tpl', page='analytics')

<div class="container" style="margin: 20px auto;">

<h2>Analytics</h2>


<div class="row">
  <div class="col-md-12">
    <h3>Dimension frequency distribution</h3>
    <p class="text-justify">Distribution of distinct LSD dimensions according to the frequency in which they appear in LOD datasets.</p>
    <div id="chart_div" style="width: auto; height: 400px;"></div>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
          var data = google.visualization.arrayToDataTable([
            ['Dimension', 'Frequency'],
          % for df in dims_freqs:
            ['{{df[0]}}', {{df[1]}}],
          % end
            ['','']
          ]);
            
        var options = {
          legend: 'none',
          title: 'Dimension frequency',
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }
    </script>

  </div>
</div>
<div class="row">
  <div class="col-md-12">
    <h3>Datasets using qb:DimensionProperty</h3>
    <p class="text-justify">Proportion of LOD datasets using any qb:DimensionProperty.</p>
    <div id="piechart" style="width: auto; height: 400px;"></div>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Dimension usage', 'Share'],
          % for f in fracs:
            ['{{f[0]}}', {{f[1]}}],
          % end
            ['','']
        ]);

        var options = {
          legend: 'none',
          title: 'Share of datasets using QB dimensions',
          pieHole: 0.4
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
    </script>
  </div> 
</div>

<div class="row">
  <div class="col-md-12">
    <h3>Chart.js</h3>
    <p class="text-justify">foo bar foobar baz.</p>
    <canvas id="myChart" width="400" height="400"></canvas>
    <script>
      var ctx = document.getElementById("myChart").getContext("2d");
      var myNewChart = new Chart(ctx);
      var options = {}
      var data = {
//    labels: {{dims}},
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
      {
      label: "My Second dataset",
      fillColor: "rgba(151,187,205,0.2)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(151,187,205,1)",
      data: [28, 48, 40, 19, 86, 27, 90]
//    data: {{freqs}}
      }
      ]
      };
      var myLineChart = new Chart(ctx).Line(data, options);
    </script>
  </div>
</div>


</div>

% include('footer.tpl')

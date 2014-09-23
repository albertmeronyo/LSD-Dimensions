<!DOCTYPE html>
<html>
  <head>
    <title>LSD Dimensions (dev)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="/img/favicon.ico">
    <!-- Bootstrap -->
    <link href="/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <!-- Bootstrap core CSS -->
    <link href="/css/bootstrap.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="/css/starter-template.css" rel="stylesheet">
    <!-- Bootstrap Table -->
    <link href="/css/bootstrap-table.css" rel="stylesheet">
    <!-- Custom styles for LSD Dimensions -->
    <link href="/css/style.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="../../assets/js/html5shiv.js"></script>
      <script src="../../assets/js/respond.min.js"></script>
    <![endif]-->

    <!-- All js dependencies with async/defer attributes -->

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="//code.jquery.com/jquery.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/js/bootstrap.min.js"></script>
    <!-- Bootstrap Table -->
    <script src="/js/bootstrap-table.js"</script>
    <!-- Chart.js -->
    <script src="/js/Chart.js"></script>
    <!-- Google Analytics -->
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-54668364-1', 'auto');
      ga('send', 'pageview');
    </script>
  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">LSD Dimensions</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
% if page == 'home':
            <li class="active"><a href="/dimensions">Home</a></li>
% else:
            <li><a href="/dimensions">Home</a></li>
% end
% if page == 'about':
	    <li class="active"><a href="/about">About</a></li>
% else:
	    <li><a href="/about">About</a></li>
% end
% if page == 'analytics':
	    <li class="active"><a href="/analytics">Analytics</a></li>
% else:
	    <li><a href="/analytics">Analytics</a></li>
% end
            <li><a href="https://github.com/albertmeronyo/lsd-dimensions" target="_blank">GitHub</a></li>
            <li><a href="mailto:albert.meronyo@gmail.com">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <div class="container">

      <div class="starter-template">

	<h1>LSD Dimensions (dev)</h1>



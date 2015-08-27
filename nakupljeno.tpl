<!DOCTYPE html>
<html lang="sl">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="/static/slika.ico">

    <title>Festivalsko poletje</title>
    
    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="jumbotron.css" rel="stylesheet">
    <link href="/static/gumbi.css" rel="stylesheet">
    <link href="/static/besede.css" rel="stylesheet">
    <link href="/static/ozadje.css" rel="stylesheet">
    <link href="/static/barcolor.css" rel="stylesheet">
    <link href="/static/napisbar.css" rel="stylesheet">
    <link href="/static/komentar.css" rel="stylesheet">


    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Festivalsko poletje</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <form class="navbar-form navbar-right">
          </form>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        %if napaka:
        <div class="alert alert-danger" role="alert">{{napaka}}</div>
        %elif napaka1:
	<div class="alert alert-danger" role="alert">{{napaka1}}</div>
	%else:
	<h2>Število vstopnic, ki ste jih nakupili je: <b>{{ kolicina }}</b></h2>
        <h3>Cena nakupa znaša: <b>{{cena_skupaj}} €</b></h3>
	%end
      </div>
    </div>

    <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-4">
          %if napaka == None and napaka1 == None:
	  <h3>Hvala za nakup!</h3>
	  %else:
	  <p></p>
          %end
        </div>
        <div class="col-md-4">
         
       </div>
        <div class="col-md-4">
        
        </div>
      </div>

      <hr>

      <footer>
        <p>&copy; Nina Potočnik</p>
      </footer>
    </div> <!-- /container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
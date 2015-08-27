
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
            <div class="form-group">
          </form>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        %for ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic, st_prodanih_festival, id in podatki:
		<h2> <b>{{ ime }}</b> </h2>
		<p>Lokacija : <b>{{ lokacija }}</b> </p>
		<p>Datum začetka : <b>{{ datum_zacetek }}</b> </p>
		<p>Datum konca: <b>{{ datum_konec }}</b> </p>
		<p>Cena : <b>{{ cena }} € </b> </p>
		<p>Število vstopnic : <b>{{ stevilo_vstopnic }}</b> </p>
		<p>Število prodanih vstopnic : <b>{{ st_prodanih_festival }}</b> </p>
	%end
      </div>
    </div>

    <div class="container">
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-4">
         <h2> Nastopajoči: </h2>
	  <ul>
	  %for id, glasbenik in nastopi:
	      <li><a href="glasbenik/{{id}}">{{ glasbenik }}</a>
	  %end
	  </ul>
	  <h3> Dodaj nastopajoče </h3>
	  %for ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic, st_prodanih_festival, id in podatki:
 	  <form action="{{id}}/dodaj_nastopajoce/" method="POST">
	    <p><input type="text" name="glasbenik" placeholder="Glasbenik..."></p>
	    <p><input style="width:175px;"type="date" name="datum" placeholder="Datum..."></p>
       	    <p><button class="btn btn-default">Dodaj</button></p>
       	  </form>
	  %end 
	  </ul>
       </div>
       <div class="col-md-4">
          <div class="panel panel-primary">
	  <div class="panel-heading">
	    <h3 class="panel-title">Komentarji</h3>
	  </div>
	  <div class="panel-body">
	   <ul>
	   %for id, uporabnisko_ime, komentar in komentarji:
		<li>{{uporabnisko_ime}}: {{komentar}}</li>
 	   %end
	   </ul>
	   </div>
 	</div>
	  <p></p>
	  <form action="{{id}}/komentar/" method="POST">
	    <p><textarea rows="4" cols="48" class = "komentar" name="komentar" placeholder="Komentar..."></textarea>
	    
	    <p><input type="text" name="uporabnisko_ime" placeholder="Uporabniško ime..."></p>
	    <p><button class="btn btn-default">Dodaj</button></p>
	  </form>
        </div>
        <div class="col-md-4">
          %for ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic, st_prodanih_festival, id in podatki:
          <form action="/{{id}}/nakup_vstopnice/">
       	  <p><a class="btn btn-lg btn-default" href="/{{id}}/nakup_vstopnice/" role="button">Nakup vstopnice</a></p>
       	  </form>
	  %end
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

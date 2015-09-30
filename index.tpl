<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@DRFbot の コーナー3-cycle (DRFバッファ) 手順一覧</title>
<meta name="description" content="Buffer is DRF!! @DRFbot の コーナー3-cycle (DRFバッファ) 手順一覧">
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">
<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
<style>
  body {
    padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
  }
  .first {
    border-top: 2px solid #DDD;
  }
</style>
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
      <a class="navbar-brand" href="#">Buffer is DRF!!</a>
    </div>
    <div id="navbar" class="collapse navbar-collapse">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">Home</a></li>
        <li><a href="https://twitter.com/DRFbot"><i class="fa fa-twitter fa-lg"></i> @DRFbot</a></li>
        <li><a href="https://github.com/kotarot/drf-bot"><i class="fa fa-github fa-lg"></i> Fork me on GitHub</a></li>
      </ul>
    </div><!--/.nav-collapse -->
  </div>
</nav>

<div class="container">

  <h1>Buffer is DRF!!</h1>
  <p><a href="https://twitter.com/DRFbot">@DRFbot</a> は Twitter上のbotです。定期的にDRFバッファのコーナー3-cycle手順を画像付きでつぶやきます。</p>

  <h3>遊び方</h3>
  <p>例えば、「@DRFbot DRF DFL RUF」、「@DRFbot DFL RUF」、または「@DRFbot ルービックキューブ 世界記録」みたいにリプライを飛ばしてみてください。</p>

  <h3>コーナー3-cycle手順一覧</h3>
  <p>現在のコーナー3-cycle (DRFバッファ) 手順一覧です。もっと良い手順を知ってたり思いついたらリプライで知らせてください。</p>

  <table class="table table-condensed table-striped">
    <thead>
      <tr><th>Cycle</th><th>手順</th><th>分類</th></tr>
    </thead>
    <tbody>
      {% for rows in rows -%}
        {{ row }}
      {%- endfor %}
    </tbody>
  </table>

</div><!-- /.container -->

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

</body>
</html>

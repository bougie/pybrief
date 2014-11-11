{% load staticfiles %}
<!DOCTYPE html>
<html lang="fr">
	<head>
		<title>{{page_title}}</title>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">

		<meta name="viewport" content="width=device-width, initial-scale=1.0">

		<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}" />
		<link rel="stylesheet" href="{% static 'css/style.css' %}" />
		<link rel="stylesheet" href="{% static 'css/pygments.css' %}" />
	</head>
	<body>
		<div class="blog-masthead">
			<div class="container">
				<nav class="blog-nav">
					<a class="blog-nav-item" href="{% url 'index' %}">Accueil</a>
					<a class="blog-nav-item" href="{% url 'blog_index' %}">Blog</a>
				</nav>
			</div>
		</div>

		<div class="container">
			<div class="blog-header">
				<h1 class="blog-title">La cave de bougie</h1>
			</div>

			{% block content %}
			{% endblock %}
		</div>

		<div class="blog-footer">
			§§§ APPARTLAND FTW §§§
		</div>

		<script type="text/javascript" src="{% static 'js/jquery.min.js' %}"></script>
		<script type="text/javascript" src="{% static 'js/bootstrap.min.js' %}"></script>
	</body>
</html>

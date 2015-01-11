{% load staticfiles %}
<!DOCTYPE html>
<html lang="fr">
	<head>
		<title>{{page_title}}</title>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">

		{% if BLOG_AUTHOR %}
			<meta name="author" content="{{BLOG_AUTHOR}}" />
		{% endif %}
		{% if BLOG_DESCRIPTION %}
			<meta name="keywords" content="{{BLOG_DESCRIPTION}}" />
		{% endif %}
		{% if BLOG_KEYWORDS %}
			<meta name="description" content="{{BLOG_KEYWORDS}}" />
		{% endif %}

		<meta name="viewport" content="width=device-width, initial-scale=1.0">

		<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}" />
		<link rel="stylesheet" href="{% static 'css/style.css' %}" />
		<link rel="stylesheet" href="{% static 'css/pygments.css' %}" />
	</head>
	<body>
		<div class="blog-masthead">
			<div class="container" id="#top">
				<nav class="blog-nav">
					{% if nav_current_module == 'index' %}
						<a class="blog-nav-item active" href="{% url 'index' %}">Accueil</a>
					{% else %}
						<a class="blog-nav-item" href="{% url 'index' %}">Accueil</a>
					{% endif %}

					{% if nav_current_module == 'blog' %}
						<a class="blog-nav-item active" href="{% url 'blog_index' %}">Blog</a>
					{% else %}
						<a class="blog-nav-item" href="{% url 'blog_index' %}">Blog</a>
					{% endif %}
					{% if nav_current_module == 'bookmarks' %}
						<a class="blog-nav-item active" href="{% url 'bookmarks_index' %}">Marque-pages</a>
					{% else %}
						<a class="blog-nav-item" href="{% url 'bookmarks_index' %}">Marque-pages</a>
					{% endif %}
				</nav>
			</div>
		</div>

		<div class="container">
			<div class="blog-header">
				<h1 class="blog-title"><span class="glyphicon glyphicon-home"></span>&nbsp;{{BLOG_TITLE}}</h1>
				<p class="lead blog-description">{{BLOG_SUBTITLE}}</p>
			</div>

			{% block content %}
			{% endblock %}
		</div>

		<div class="blog-footer">
			<a href="#top">Remonter</a><br />
			§§§ APPARTLAND FTW §§§
		</div>

		<script type="text/javascript" src="{% static 'js/jquery.min.js' %}"></script>
		<script type="text/javascript" src="{% static 'js/bootstrap.min.js' %}"></script>
		<script type="text/javascript" src="{% static 'js/script.js' %}"></script>
	</body>
</html>

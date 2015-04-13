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
		<link rel="stylesheet" href="{% static 'css/bookmarks/style.css' %}" />
		<link rel="stylesheet" href="{% static 'css/pygments.css' %}" />
	</head>
	<body>
		<div class="container">
			{% block content %}
			{% endblock %}
		</div>

		<script type="text/javascript" src="{% static 'js/jquery.min.js' %}"></script>
		<script type="text/javascript" src="{% static 'js/bootstrap.min.js' %}"></script>
		<script type="text/javascript" src="{% static 'js/bookmarks/script.js' %}"></script>
	</body>
</html>

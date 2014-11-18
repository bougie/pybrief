{% extends 'base.tpl' %}

{% block content %}
	{% if post %}
	<div class="jumbotron">
		<h2>Dernier billet</h2>

		<h3>{{post.title}}</h3>
		{{post.description_html|safe}}
		<a href="{% url 'blog_post' post.id post.slug %}" class="btn btn-primary btn-sm">Lire la suite</a>
	</div>
	{% endif %}

	{% if posts %}
	<div class="row">
		<div class="col-lg-8">
			<h2>Billets recents</h2>

			{% for post in posts %}
			<a href="{% url 'blog_post' post.id post.slug %}">{{post.title}}</a><br />
			{% endfor %}
		</div>
	</div>
	{% endif %}
{% endblock %}

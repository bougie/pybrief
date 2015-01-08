{% extends 'base.tpl' %}

{% block content %}
	{% if post %}
	<div class="jumbotron">
		<h2><span class="glyphicon glyphicon-book"></span>&nbsp;Dernier billet</h2>

		<h3>{{post.title}}</h3>
		{{post.description_html|safe}}
		<a href="{% url 'blog_post' post.id post.slug %}" class="btn btn-primary btn-sm">Lire la suite</a>
	</div>
	{% endif %}

	{% if posts %}
	<div class="row">
		<div class="col-lg-5">
			<h2><span class="glyphicon glyphicon-list"></span>&nbsp;Billets recents</h2>

			{% for post in posts %}
			<a href="{% url 'blog_post' post.id post.slug %}" title="Le {{post.create_date|date:"d/m/Y à H:i"}} par {{post.author}}">
				{{post.title}}
			</a><br />
			{% endfor %}
		</div>
		<div class="col-lg-7">
			<h2><span class="glyphicon glyphicon-link"></span>&nbsp;Marques pages recents</h2>

			{% for link in links %}
			<a href="{{link.url}}">
				{% if link.name %}
					{{link.name}}
				{% elif link.title %}
					{{link.title}}
				{% elif link.url %}
					{{link.url}}
				{% endif %}
			</a><br />
			{% endfor %}
		</div>
	</div>
	{% endif %}
{% endblock %}

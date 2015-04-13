{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
<div class="row">
	<div class="col-sm-10 blog-main">
		<div class="blog-post">
			<h2 class="blog-post-title">{{post.title}}</h2>

			{{post.content_html|safe}}
		</div>
	</div>

	<div class="col-sm-2 blog-sidebar">
		<div class="sidebar-module sidebar-module-inset">
			<h4><span class="glyphicon glyphicon-info-sign"></span>&nbsp;A propos</h4>
			<div class="text-center">
				<img src="{% static 'img/noavatar.png' %}" alt="noavatar" /><br />
			</div>
			Par <a href="{% url 'blog_posts_author' post.author %}">{{post.author}}</a> le {{post.create_date|date:"d/m/Y à H:i"}}
		</div>

		{% if post.tags.all|length > 0 %}
		<div class="sidebar-module sidebar-module">
			<h4><span class="glyphicon glyphicon-tags"></span>&nbsp;Tags</h4>

			{% for tag in post.tags.all %}
				<a href="{% url 'blog_posts_tag' tag.name %}">{{tag.name}}</a>
			{% endfor %}
		</div>
		{% endif %}
	</div>
</div>
{% endblock %}

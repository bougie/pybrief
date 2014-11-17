{% extends 'base.tpl' %}

{% block content %}
<div class="row">
	<div class="col-sm-8 blog-main">
		<div class="blog-post">
			<h2 class="blog-post-title">{{post.title}}</h2>

			{{post.content_html|safe}}
		</div>
	</div>

	<div class="col-sm-3 col-sm-offset-1 blog-sidebar">
		<div class="sidebar-module sidebar-module-inset">
			<h4>A propos</h4>
			Par <a href="#">{{post.author}}</a> le {{post.create_date|date:"d/m/Y à H:i"}}
		</div>

		{% if post.tags %}
		<div class="sidebar-module sidebar-module">
			<h4>Classé dans</h4>

			{% for tag in post.tags.all %}
				<a href="{% url 'blog_posts_tag' tag.name %}">{{tag.name}}</a>
			{% endfor %}
		</div>
		{% endif %}
	</div>
</div>
{% endblock %}

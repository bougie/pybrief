{% extends 'base.tpl' %}

{% block content %}
<div class="row">
	<div class="col-sm-12 blog-main">
		{% for post in posts %}
		<div class="blog-post">
			<h2 class="blog-post-title">{{post.title}}</h2>
			<p class="blog-post-meta">le {{post.create_date|date:"d/m/Y à H:i"}} par <a href="#">{{post.author}}</a></p>

			{{post.description_html|safe}}
		</div>
		{% endfor %}
	</div>
</div>
{% endblock %}

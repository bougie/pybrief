{% extends 'base.tpl' %}

{% block content %}
<div class="row">
	<div class="col-sm-8 blog-main">
		{% for post in posts %}
		<div class="blog-post">
			<h2 class="blog-post-title">{{post.title}}</h2>
			<p class="blog-post-meta">{{post.date}} by <a href="#">{{post.author}}</a></p>

			{{post.content}}
		</div>
		{% endfor %}
	</div>

	<div class="col-sm-3 col-sm-offset-1 blog-sidebar">
		<div class="sidebar-module sidebar-module-inset">
			<h4>About</h4>
			<p>Kewkew tout le monde les gens</p>
		</div>

		<div class="sidebar-module">
			<h4>Tags</h4>
		</div>
	</div>
</div>
{% endblock %}

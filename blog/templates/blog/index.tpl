{% extends 'base.tpl' %}

{% block content %}
<div class="row">
	<div class="col-sm-8 blog-main">
		{% for post in posts %}
		<div class="blog-post">
			<h2 class="blog-post-title">
				<a href="{% url 'blog_post' post.id post.slug %}">{{post.title}}</a>
			</h2>
			<p class="blog-post-meta">le {{post.create_date|date:"d/m/Y à H:i"}} par <a href="{% url 'blog_posts_author' post.author %}">{{post.author}}</a></p>

			{{post.content_html|safe}}
		</div>
		{% endfor %}

		<nav>
			<ul class="pager">
				{% if posts.has_previous %}
					<li><a href="?page={{posts.previous_page_number}}">&lt;- Plus récent</a></li>
				{% endif %}
				{% if posts.has_next %}
					<li><a href="?page={{posts.next_page_number}}">Plus vieux -&gt;</a></li>
				{% endif %}
			</ul>
		</nav>
	</div>

	<div class="col-sm-3 col-sm-offset-1 blog-sidebar">
		{% if BLOG_DESCRIPTION %}
			<div class="sidebar-module sidebar-module-inset">
				<h4>About</h4>
				<p>{{BLOG_DESCRIPTION}}</p>
			</div>
		{% endif %}

		<div class="sidebar-module">
			<h4>Tags</h4>

			{% for tag in tags %}
				<a href="{% url 'blog_posts_tag' tag.name %}">{{tag.name}}</a>
			{% endfor %}
		</div>
	</div>
</div>
{% endblock %}

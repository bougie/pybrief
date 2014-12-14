{% extends 'base.tpl' %}

{% block content %}
{% for post in posts %}
	<div class="row blog-main blog-post blog-item-line">
		<div class="col-sm-offset-1 col-sm-2">
			<p class="blog-post-meta text-center">
				<a href="{% url 'blog_posts_author' post.author %}">{{post.author}}</a></br >
			</p>
		</div>
		<div class="col-sm-9">
			<h2 class="blog-post-title">
				<a href="{% url 'blog_post' post.id post.slug %}">{{post.title}}</a>
			</h2>
			<p class="blog-post-meta">
				le {{post.create_date|date:"d/m/Y à H:i"}}<br />
				tags: {% for tag in post.tags.all %}<a href="{% url 'blog_posts_tag' tag.name %}">{{tag.name}}</a>&nbsp;{% endfor %}
			</p>

			{{post.description_html|safe}}
		</div>
	</div>
{% endfor %}

<div class="row">
	<div class="col-sm-12">
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
</div>
{% endblock %}

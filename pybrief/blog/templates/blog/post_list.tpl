{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
{% if submodule == 'tag' %}
	<h2 class="blog-subtitle">Billets taggés '{{tagname}}'</h2>
{% elif submodule == 'author' %}
	<h2 class="blog-subtitle">Billets écrits par {{author}}</h2>
{% elif submodule == 'archives' %}
	<h2 class="blog-subtitle">Billets du {{month}}/{{year}}</h2>
{% endif %}

{% for post in posts %}
	<div class="row blog-main blog-post blog-item-line">
		<div class="col-sm-2">
			<p class="blog-post-meta text-center">
				<img src="{% static 'img/noavatar.png' %}" alt="noavatar" />
				<a href="{% url 'blog_posts_author' post.author %}">{{post.author}}</a>
			</p>
		</div>
		<div class="col-sm-9">
			<h2 class="blog-post-title">
				<a href="{% url 'blog_post' post.id post.slug %}">{{post.title}}</a>
			</h2>
			<p class="blog-post-meta">
				le {{post.create_date|date:"d/m/Y à H:i"}}<br />
				<span class="glyphicon glyphicon-tags"></span>&nbsp;{% for tag in post.tags.all %}<a href="{% url 'blog_posts_tag' tag.name %}">{{tag.name}}</a>&nbsp;{% endfor %}
			</p>

			{{post.description_html|safe}}
		</div>
	</div>
{% endfor %}

<div class="row">
	<div class="col-sm-12">
		<nav>
			<ul class="pager">
				{% if page_obj.has_previous %}
					<li><a href="?page={{page_obj.previous_page_number}}"><span class="glyphicon glyphicon-arrow-left"></span></a></li>
				{% endif %}
				{% if page_obj.has_next %}
					<li><a href="?page={{page_obj.next_page_number}}"><span class="glyphicon glyphicon-arrow-right"></span></a></li>
				{% endif %}
			</ul>
		</nav>
	</div>
</div>
{% endblock %}

{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
<div class="row">
	<div class="col-sm-10">
		<form action="{% url 'bookmarks_add' %}" method="POST" class="form-horizontal" style="display: none;" id="add-bookmark">
			{% csrf_token %}
			{% for field in form %}
			<div class="form-group">
				<label for="{{field.name}}" class="col-sm-1 control-label">{{field.name}}</label>
				<div class="col-sm-11">
					<input type="text" name="{{field.name}}" id="{{field.name}}" class="form-control" placeholder="{{field.name}}" />
				</div>
			</div>
			{% endfor %}

			<div class="send text-right">
				<button type="submit" class="btn btn-default">Ajouter</button>
			</div>
		</form>

		<table class="table">
			{% for link in links %}
			<tr>
				<td class="text-center">
					<img src="{% static 'img/nothumb.png' %}" alt="nothumb" />
				</td>
				<td>
					<div>
						{% if link.name %}
						<a href="{{link.url}}" class="link-title">{{link.name}}</a>
						{% elif link.title %}
						<a href="{{link.url}}" class="link-title">{{link.title}}</a>
						{% else %}
						<a href="{{link.url}}" class="link-title">{{link.url}}</a>
						{% endif %}
						{% if link.domain %}
						<div class="link-description">by {{link.domain}}</div>
						{% endif %}
					</div>
					{% if link.tags.all|length > 0 %}
					<div class="text-right">
						{% for tag in link.tags.all %}
							<a class="tag_box" href="{% url 'bookmarks_links_tag' tag.name %}">{{tag.name}}</a>
						{% endfor %}
					</div>
					{% endif %}
				</td>
			</tr>
			{% endfor %}
		</table>

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
	<div class="col-sm-2">
		<div class="send text-right">
			<a href="#" id="add-bookmark-link" class="btn btn-default">Nouveau marque-page</a>
		</div>
	</div>
</div>
{% endblock %}

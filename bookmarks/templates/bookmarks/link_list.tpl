{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
<div class="row">
	<div class="col-sm-10">
		<form action="{% url 'bookmarks_add' %}" method="POST" class="form-horizontal" style="display: none;" id="form-bookmark">
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
				<button type="submit" class="btn btn-primary">Valider</button>
				<button type="button" class="btn btn-cancel" id="btn-cancel">Annuler</button>
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

						<a href="#" class="btn btn-default btn-xs edit-link" style="visibility: visible;" id="link-id-{{link.id}}"><span class="glyphicon glyphicon-edit"></span></a>

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
		<div class="sidebar-module sidebar-module-inset text-center">
			<a href="#" id="add-bookmark-link" class="btn btn-default"><span class="glyphicon glyphicon-link"></span>&nbsp;Nouveau marque-page</a>
		</div>
		<div class="sidebar-module">
			<h4><span class="glyphicon glyphicon-tags"></span>&nbsp;&nbsp;Tags</h4>

			{% for tag in tags %}
				<a href="{% url 'bookmarks_links_tag' tag.name %}">{{tag.name}}</a>
			{% endfor %}
		</div>

		<div class="sidebar-module">
			<h4><span class="glyphicon glyphicon-hand-right"></span>&nbsp;Outils</h4>

			<a class="" href="javascript:(function(){window.open('{{share_link}}?u='+encodeURIComponent(window.location));})()" id="bookmarkme" title="{{share_title}}" rel="sidebar">Create bookmarklet</a>
		</div>
	</div>
</div>
{% endblock %}

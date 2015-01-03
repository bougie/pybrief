{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
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
				{% for tag in link.tags.all %}{{tag.name}}{% endfor %}
			</div>
			{% endif %}
		</td>
	</tr>
	{% endfor %}
</table>
{% endblock %}

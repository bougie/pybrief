{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
<table class="table table-striped">
	{% for link in links %}
	<tr>
		<td>
			{% if link.name %}
			<a href="{{link.url}}">{{link.name}}</a>
			{% else %}
			<a href="{{link.url}}">{{link.title}}</a>
			{% endif %}
		</td>
	</tr>
	{% endfor %}
</table>
{% endblock %}

{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
<table class="table table-striped">
	<tr>
		<th>Lien</th>
	</tr>
	{% for link in links %}
	<tr>
		<td><a href="{{link.url}}">{{link.name}}</a></td>
	</tr>
	{% endfor %}
</table>
{% endblock %}

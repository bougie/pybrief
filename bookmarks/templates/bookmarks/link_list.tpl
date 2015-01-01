{% extends 'base.tpl' %}
{% load staticfiles %}

{% block content %}
<table class="table">
	{% for link in links %}
	<tr>
		<td>
			<div>
				{% if link.name %}
				<a href="{{link.url}}">{{link.name}}</a>
				{% else %}
				<a href="{{link.url}}">{{link.title}}</a>
				{% endif %}
				{% if link.domain %}
				<div class="">by {{link.domain}}</div>
				{% endif %}
			</div>
			<div class="text-right">
				#link #blabla
			</div>
		</td>
	</tr>
	{% endfor %}
</table>
{% endblock %}

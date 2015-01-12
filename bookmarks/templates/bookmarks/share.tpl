{% extends 'base_empty.tpl' %}

{% block content %}
<form action="{% url 'bookmarks_add' %}" method="POST" class="form-horizontal" id="form-bookmark">
	{% csrf_token %}

	{% for field in form %}
		<div class="form-group">
			<label for="{{field.name}}" class="col-sm-1 control-label">{{field.name}}</label>
			<div class="col-sm-11">
				<input type="text" name="{{field.name}}" id="{{field.name}}" class="form-control" placeholder="{{field.name}}" value="{% if field.value %}{{field.value}}{% endif %}" />
			</div>
		</div>
	{% endfor %}

	<div class="send text-right">
		<button type="submit" class="btn btn-primary">Partager</button>
		<button type="button" class="btn btn-cancel" id="btn-cancel">Annuler</button>
	</div>
</form>
{% endblock %}

function display_add_bookmark_block(id) {
	if($('#' + id + ':hidden').length == 0) {
		$('#' + id).hide();
	} else {
		$('#' + id).show();
	}
}

$(function() {
	$('#add-bookmark-link').on('click', function() {
		display_add_bookmark_block('add-bookmark');
	});
});

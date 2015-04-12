/*
 * Show or hide (depends on the current state) the add/edit bookmarks form
 */
function display_form_bookmark_block(id, force_hide) {
	if($('#' + id + ':hidden').length == 0 || force_hide == true) {
		$('#' + id).hide();

		$('#' + id).attr('action', '/bookmarks/new');
		$('#' + id).attr('method', 'POST');
	} else {
		$('#' + id).show();
	}
}

/*
 * Populate and display the add/edit bookmarks form
 */
function display_edit_bookmark_block(formid, linkid) {
	if(linkid != undefined) {
		linkid = linkid.split('-')[2];

		$.getJSON('/bookmarks/edit/' + linkid, function(data) {
			$('#' + formid).attr('action', data.form_action);
			$('#' + formid).attr('method', data.form_method);

			$('#' + formid + ' #url').val(data.link.url);
			$('#' + formid + ' #name').val(data.link.name);
			$('#' + formid + ' #tags').val(data.link.tags);
		});

		if($('#' + formid + ':hidden').length != 0) {
			$('#' + formid).show();

			$('#add-bookmark-link').on('click', function() {
				cancel_form_bookmark('form-bookmark');
				display_form_bookmark_block('form-bookmark', false);
			});
		}
	}
}

/*
 * Empty and hide add/edit bookmarks form
 */
function cancel_form_bookmark(formid) {
	display_form_bookmark_block(formid, true);

	$('#' + formid + ' #url').val('');
	$('#' + formid + ' #name').val('');
	$('#' + formid + ' #tags').val('');
}

$(function() {
	$('#add-bookmark-link').on('click', function() {
		display_form_bookmark_block('form-bookmark', false);
	});

	$('.edit-link').on('click', function() {
		display_edit_bookmark_block('form-bookmark', $(this).attr('id'));
	});

	$('#form-bookmark #btn-cancel').on('click', function() {
		cancel_form_bookmark('form-bookmark');
	});
});

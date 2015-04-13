function favoris(share_link, share_title) {
	link = "javascript:(function(){window.open("+share_link+"+\"?u=\"+encodeURIComponent(window.location));})()";

	if(window.external) { // IE Favorite
		window.external.AddFavorite(link, share_title);
	} else if(window.opera && window.print) { // Opera Hotlist
		this.title = document.title;
	}

	return false;
}

$(function() {
	$('#bookmarkme').on('click', function() {
		favoris($(this).attr('href'), $(this).attr('title'));
	});
});

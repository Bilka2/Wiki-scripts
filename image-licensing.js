//Marks pages as game image or screenshot by prepending the appropriate template
//Both params are arrays of full page names. Example: var screenshots = ["File:2to4 balancer.png", "File:12to12 balancer.png"];
function function licenseImages(gameImages, screenshots) {
	getToken();
	var GameImagesCategorymembers = getCategorymembers('Category:Game_images');
	for (var i = 0; i < gameImages.length; i++) {
		var title = gameImages[i];
		if (!GameImagesCategorymembers[title] && !isPageRedirect(title)) {
			prependEditPage(title, '{{Game image}}', 'Categorised file as game image.');
		}
	}
	var screenshotsCategorymembers = getCategorymembers('Category:Screenshots');
	for (var j = 0; j < screenshots.length; j++) {
		var title = screenshots[j];
		if (!screenshotsCategorymembers[title] && !isPageRedirect(title)) {
			prependEditPage(title, '{{Screenshot}}', 'Categorised file as screenshot.');
		}
	}
};

function getCategorymembers(category) {
	var object = {};
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'categorymembers',
			cmtitle: category,
			cmlimit: 600,
			cmprop: 'title'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var categorymembers = data.query.categorymembers;
			console.log('Found ' + categorymembers.length + ' pages in ' + category);
			for (var i = 0; i < categorymembers.length; i++) {
				object[categorymembers[i].title] = true;
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
	return object;
};

function prependEditPage(title, content, summary) {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'edit',
			title: title,
			prependtext: content,
			token: globalToken,
			summary: summary,
			bot: true,
			nocreate: true
		},
		async: false,
		dataType: 'json',
		type: 'POST',
		success: function( data ) {
			console.log("Edited " + title);
		},
		error: function( xhr ) {
			alert("Failed to edit " + title);
		}
	});
};

function isPageRedirect(title) {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: title,
			prop: 'info'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var page = data.query.pages[Object.keys(data.query.pages)[0]];
			if (page["redirect"]) {
				return true;
			} else {
				return false;
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
};
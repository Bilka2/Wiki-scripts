var i = 0;
var ind = 0;
$("#js-test").click(function(){
    getInfoboxPages();
});
function getInfoboxPages() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	getToken();
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			list: 'categorymembers',
			cmtitle: 'Category:Infobox_page',
			cmlimit: 400,
			cmprop: 'title',
			cmcontinue: 'page|4348454d495354525920285245534541524348292f494e464f424f58|38720' //skip the pages that I botched (up to chemical plant)
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var categorymembers = data.query.categorymembers;
			console.log('Found ' + categorymembers.length + ' infobox pages.');
			setTimeout(function(){getPagesUsingInfobox(categorymembers, categorymembers[0].title)}, 500);
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
}

function getPagesUsingInfobox(categorymembers, infoboxPage) {
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			list: 'embeddedin',
			eititle: infoboxPage,
			eilimit: 500,
			eifilterredir: 'nonredirects',
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var embeddedin = data.query.embeddedin;
			if (embeddedin.length == 0) {
				console.log('No pages transclude ' + infoboxPage);
				setTimeout(function(){moveInfoboxPage(infoboxPage, categorymembers)}, 500);
			} else {
				console.log(embeddedin.length + ' pages transclude ' + infoboxPage + '.');
				setTimeout(function(){changePageUsingInfobox(infoboxPage, embeddedin, embeddedin[0].title, categorymembers)}, 500);
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
}

function changePageUsingInfobox(infoboxPage, embeddedin, pageUsingInfobox, categorymembers) {
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			titles: pageUsingInfobox,
			prop: 'revisions',
			rvprop: 'content'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var revisions = pages[Object.keys(pages)[0]].revisions[0];
			var content = revisions[Object.keys(revisions)[2]];
			setTimeout(function(){editPageUsingInfobox(infoboxPage, embeddedin, pageUsingInfobox, content, categorymembers)}, 200);
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
}

function editPageUsingInfobox(infoboxPage, embeddedin, pageUsingInfobox, content, categorymembers) {
	var searchString = "{{:" + infoboxPage + "}}";
	var posi = infoboxPage.search("/infobox");
	var newInfoboxPage = infoboxPage.slice(0,posi);
	var replaceString = "{{:Infobox:" + newInfoboxPage + "}}";
	var newContent = content.replace(searchString, replaceString)
	
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'edit',
			title: pageUsingInfobox,
			text: newContent,
			token: globalToken,
			summary: 'New infobox organization.',
			bot: true,
			nocreate: true
		},
		async: false,
		dataType: 'json',
		type: 'POST',
		success: function( data ) {
			console.log('Changed ' + pageUsingInfobox);	
			ind++;
			if (ind + 1 > embeddedin.length) {
				console.log("Changed all pages that transclude " + infoboxPage + ".");
				ind = 0;
				setTimeout(function(){moveInfoboxPage(infoboxPage, categorymembers)}, 500);
			} else {
				setTimeout(function(){changePageUsingInfobox(infoboxPage, embeddedin, embeddedin[ind].title, categorymembers)}, 500);
			}
		},
		error: function( xhr ) {
			alert('Failed to change ' + pageUsingInfobox);
		}
	});
}

function moveInfoboxPage(infoboxPage, categorymembers) {
	var posi = infoboxPage.search("/infobox");
	var newInfoboxPage = infoboxPage.slice(0,posi);
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'move',
			token: globalToken,
			from: infoboxPage,
			to: 'Infobox:' + newInfoboxPage,
			ignorewarnings: true,
			reason: 'New infobox organization.',
			noredirect: true,
			movetalk: true,
			movesubpages: true
		},
		async: false,
		dataType: 'json',
		type: 'POST',
		success: function(data) {
			console.log('Moved ' + infoboxPage + ' to Infobox:' + newInfoboxPage + '.');
			i++;
			if (i + 1 > categorymembers.length) {
				console.log("Job's done!");
				i = 0;
				return;
			} else {
				setTimeout(function(){getPagesUsingInfobox(categorymembers, categorymembers[i].title)}, 500);
			}
		},
		error: function(xhr) {
			alert( 'Error: Request failed. Could not move ' + infoboxPage + '.');
		}
	});
}

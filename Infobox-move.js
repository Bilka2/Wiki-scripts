var i = 0;
var ind = 0;
$("#js-test").click(function(){
    getInfoboxPages();
});
function getInfoboxPages() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	getToken();
	var infoboxPages = [];
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			list: 'categorymembers',
			cmtitle: 'Category:Infobox_page',
			cmlimit: 400,
			cmprop: 'title',
			cmcontinue: 'page|4143544956452050524f56494445522043484553542f494e464f424f58|38711' //skip accumulator
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
	console.log("Getting pages that transclude " + infoboxPage);
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
			console.log(embeddedin.length + ' pages transclude ' + infoboxPage + '.');
			setTimeout(function(){changePageUsingInfobox(infoboxPage, embeddedin, embeddedin[0].title, categorymembers)}, 500);
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
		},
		error: function( xhr ) {
			console.log('Failed to change ' + pageUsingInfobox);
		}
	});
		
	ind++;
	if (ind + 1 > embeddedin.length) {
		console.log("Changed all pages that transclude " + infoboxPage + ".");
		setTimeout(function(){moveInfoboxPage(infoboxPage, categorymembers)}, 500);
	} else {
		setTimeout(function(){changePageUsingInfobox(infoboxPage, embeddedin, embeddedin[ind].title, categorymembers)}, 500);
	}
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
		},
		error: function(xhr) {
			console.log( 'Error: Request failed. Could not move ' + infoboxPage + '.');
		}
	});
	
	i++;
	if (i + 1 > categorymembers.length) {
		console.log("Job's done!");
		return;
	} else {
		setTimeout(function(){getPagesUsingInfobox(categorymembers, categorymembers[i].title)}, 500);
	}
}

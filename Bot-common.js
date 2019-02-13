function lowercaseFirstLetter(string) {
	return string.charAt(0).toLowerCase() + string.slice(1);
};

/* Change links pointing to a redirect */

$("#change-links-to-redirect").click(function(){
	getRedirectToChange();
});

function getRedirectToChange() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	var redirect = prompt("Please enter the redirect. Pages linking to it will have their links changed to go to the link the redirect links to. So make sure it links to the right page!");
	if (!redirect) return;
	getToken();
	changeLinksToRedirect(redirect);
};

function changeLinksToRedirect(redirect) {
	var redirectLinks = [];
	var newLink = "";
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: redirect,
			redirects: ''
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			if (data.query.redirects) {
				newLink = data.query.redirects[0].to;
			} else {
				alert("Error! The page is not a redirect.");
				return;
			}
			if (data.query.normalized) {
				redirectLinks[0] = data.query.normalized[0].from;
				redirectLinks[1] = data.query.normalized[0].to;
			} else {
				redirectLinks[0] = redirect;
				if (redirect.replace(/\s/g, "_") != redirect) redirectLinks.push(redirect.replace(" ", "_"));
			}
			var backlinks = getBacklinks(redirect);
			var fileLink = false;
			if (redirectLinks[0].search(/File:/i) == 0) {
				fileLink = true;
				var imageusage = getFileUsage(redirect);
				//don't put imageusage into backlinks if it's already there:
				iloop3: for (var i = 0; i < imageusage.length; i++) {
					for (var j = 0; j < backlinks.length; j++) {
						if (backlinks[j].title == imageusage[i].title) {
							continue iloop3;
						}
					}
				backlinks.push(imageusage[i]);
				}
			}
			if (backlinks.length == 0) {
				alert("Nothing links there.")
				return;
			}
	
			var newNotFileLink = "";
			if (fileLink) {
				newNotFileLink = newLink.slice(5, -4);
				for (var i = 0; i < redirectLinks.length; i++) {
					if (redirectLinks[i].search(/File:/i) == 0) redirectLinks.push(redirectLinks[i].slice(5, -4));
				}
			}
			for (var i = 0; i < redirectLinks.length; i++) {
				var lowercaseLink = lowercaseFirstLetter(redirectLinks[i]);
				if (lowercaseLink != redirectLinks[i]) redirectLinks.push(lowercaseLink); //possible duplicates don't really matter here
			}
			console.log(redirectLinks)
		
			for (var i = 0; i < backlinks.length; i++) {
				$.ajax({
					url: apiUrl,
					data: {
						format: 'json',
						action: 'query',
						titles: backlinks[i].title,
						prop: 'revisions',
						rvprop: 'content'
					},
					async: false,
					dataType: 'json',
					type: 'GET',
					success: function( data ) {
						var pages = data.query.pages;
						var revisions = pages[Object.keys(pages)[0]].revisions[0];
						var oldContent = revisions[Object.keys(revisions)[2]];
						var content = oldContent;
						for (var j = 0; j < redirectLinks.length; j++) {
							while (true) {
								var tempcontent = "";
								var tempNewLink = "";
								if (fileLink) {
									tempNewLink = redirectLinks[j].search(/File:/i) == 0 ? newLink : newNotFileLink; //var value = *condition* ? *true* : *false*;
								} else {
									tempNewLink = newLink;
								}
								tempcontent = content.replace("[[" + redirectLinks[j] + "]]", "[[" + tempNewLink + "]]"); //gotta love being unable to compile a reg expr
								tempcontent = tempcontent.replace("[[" + redirectLinks[j] + " ]]", "[[" + tempNewLink + "]]");
								tempcontent = tempcontent.replace("[[" + redirectLinks[j] + "#", "[[" + tempNewLink + "#");
								tempcontent = tempcontent.replace("[[" + redirectLinks[j] + "|", "[[" + tempNewLink + "|");
								tempcontent = tempcontent.replace("[[" + redirectLinks[j] + " |", "[[" + tempNewLink + "|");
								tempcontent = tempcontent.replace("[[" + redirectLinks[j] + "  ", "[[" + tempNewLink + "  ");
								tempcontent = tempcontent.replace("{{Icon|" + redirectLinks[j] + "|", "{{Icon|" + tempNewLink + "|");
								tempcontent = tempcontent.replace("{{Icon|" + redirectLinks[j] + " |", "{{Icon|" + tempNewLink + "|");
								tempcontent = tempcontent.replace("{{icon|" + redirectLinks[j] + "|", "{{Icon|" + tempNewLink + "|");
								tempcontent = tempcontent.replace("{{icon|" + redirectLinks[j] + " |", "{{Icon|" + tempNewLink + "|");
								tempcontent = tempcontent.replace("{{Imagelink|" + redirectLinks[j] + "|", "{{Imagelink|" + tempNewLink + "|");
								tempcontent = tempcontent.replace("{{Imagelink|" + redirectLinks[j] + " |", "{{Imagelink|" + tempNewLink + "|");
								tempcontent = tempcontent.replace("{{imagelink|" + redirectLinks[j] + "|", "{{Imagelink|" + tempNewLink + "|");
								tempcontent = tempcontent.replace("{{imagelink|" + redirectLinks[j] + " |", "{{Imagelink|" + tempNewLink + "|");
								if (!fileLink) {
									tempcontent = tempcontent.replace("|" + redirectLinks[j] + "}}", "|" + tempNewLink + "}}"); //I hope this doesn't break anything
									//tempcontent = tempcontent.replace("|" + redirectLinks[j] + "|", "|" + tempNewLink + "|"); //I hope this doesn't break anything
								} else { //only done for file links
									tempcontent = tempcontent.replace("[[:" + redirectLinks[j] + "]]", "[[:" + tempNewLink + "]]");
									tempcontent = tempcontent.replace("[[:" + redirectLinks[j] + " ]]", "[[:" + tempNewLink + "]]");
									tempcontent = tempcontent.replace("[[:" + redirectLinks[j] + "|", "[[:" + tempNewLink + "|");
									tempcontent = tempcontent.replace("[[:" + redirectLinks[j] + " |", "[[:" + tempNewLink + "|");
									tempcontent = tempcontent.replace("[[:" + redirectLinks[j] + "  ", "[[:" + tempNewLink + "  ");
								}
								if (tempcontent != content) {
									content = tempcontent;
								} else {
									break;
								}
							}
						}
						if (oldContent != content) {
							genericEditPage(backlinks[i].title, content, "Changed links going to the redirect " + redirectLinks[0] + " to go to " + newLink + ".")
						} else {
							console.log("Could not correct the links on " + backlinks[i].title + " using code. Sorry about that.");
						}
					},
					error: function( xhr ) {
						alert( 'Error: Get content failed.' );
					}
				});
			}
			console.log("Done!");
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
};


/* get the number of users who ever made an edit, for conveniece */

$("#GetEditingUsers").click(function(){
    getNumberOfUsersWhoMadeEdits();
});

function getNumberOfUsersWhoMadeEdits() {
	getUserGroup();
	if (userGroup.some(isBot) == false) {
		return;
	}
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'allusers',
			aulimit: 5000,
			auwitheditsonly: true
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var allusers = data.query.allusers;
			var numberOfUsersWhoMadeEdits = data.query.allusers.length;
			console.log(numberOfUsersWhoMadeEdits)
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
};

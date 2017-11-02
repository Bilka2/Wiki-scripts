/// ONLY CONTAINS SCRIPTS THAT I MADE, MODIFIED (WANTED PAGES), OR ONES MINE DEPEND ON (NAMELY CREATEPAGE, GETTOKEN AND COMPARE) ///

var apiUrl = mw.config.get('wgServer') + mw.config.get('wgScriptPath') + "/api.php"

/* Script in here will be executed when the page is "ready" */
$(document).ready(getNumberOfActiveUsers);

/* show correct number of active users on the main page */

function getNumberOfActiveUsers() {
	if (document.getElementById("active-users")) {
		$.ajax({
			url: apiUrl,
			data: {
				format: 'json',
				action: 'query',
				list: 'allusers',
				aulimit: 500,
				auactiveusers: true
			},
			dataType: 'json',
			type: 'GET',
			success: function(data) {
				document.getElementById("active-users").innerHTML = data.query.allusers.length.toString();
			},
			error: function(xhr) {
				console.log( 'Error: Request failed.' );
			}
		});
	}
};


/* Infobox more info in header */

$(".more-button").click(function() {
  $(".more-content").toggle("fast");
});

/* Template:Inventory */

$(".tab-head-1").click(function() {
	$(".tab-head").removeClass("tab-head-active");
	$(this).addClass("tab-head-active");
	$(".tab").hide();
	$(".tab-1").show();
});

$(".tab-head-2").click(function() {
	$(".tab-head").removeClass("tab-head-active");
	$(this).addClass("tab-head-active");
	$(".tab").hide();
	$(".tab-2").show();
});

$(".tab-head-3").click(function() {
	$(".tab-head").removeClass("tab-head-active");
	$(this).addClass("tab-head-active");
	$(".tab").hide();
	$(".tab-3").show();
});

$(".tab-head-4").click(function() {
	$(".tab-head").removeClass("tab-head-active");
	$(this).addClass("tab-head-active");
	$(".tab").hide();
	$(".tab-4").show();
});

/* Wanted pages -> Factorio:Wanted_pages */

var wantedPagesListsLocation = "Factorio:Wanted pages";
var enPageLength = {};
var stubs = {};
var disambigs = {};

function getStubs() {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'categorymembers',
			cmtitle: 'Category:Stubs',
			cmlimit: 400,
			cmprop: 'title'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var categorymembers = data.query.categorymembers;
			console.log('Found ' + categorymembers.length + ' stubs.');
			for (var i = 0; i < categorymembers.length; i++) {
				stubs[categorymembers[i].title] = true;
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
};

function getDisambigs() {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'categorymembers',
			cmtitle: 'Category:Disambiguations',
			cmlimit: 400,
			cmprop: 'title'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var categorymembers = data.query.categorymembers;
			console.log('Found ' + categorymembers.length + ' disambigs.');
			for (var i = 0; i < categorymembers.length; i++) {
				disambigs[categorymembers[i].title] = true;
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
};

$("#create-wanted-pages-list").click(function(){
    getToken();
    createWantedPagesLists();
});

function createWantedPagesLists() {
    getUserGroup();
    if (userGroup.some(isBot) == false) return;
    enPageLength = {};
    var wantedPages = getWantedPages();
    console.log("Got wantedPages.");
    //wantedPages = filterWantedPages(wantedPages); //takes a lot of api requests, not worth it atm 
    //console.log("Filtered wantedPages.");
    wantedPages = wantedPages.sort(compare);
    console.log("Sorted wantedPages.");
    splitWantedPagesIntoDifferentLanguages(wantedPages);
};

function getWantedPages() {
	var wantedPages = [];

	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'querypage',
			qppage: 'Wantedpages',
			qplimit: '5000',
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var results = data.query.querypage.results;
			iloop1: for (var i = 0; i < results.length; i++) {
				var pageObject = new WantedPage(results[i].title, results[i].value);
				for (var j = 0; j < wantedPages.length; j++) {
					if (wantedPages[j].title == pageObject.title) {
						continue iloop1; //don't put page into array
					}
				}
				wantedPages.push(pageObject);
			}
		},
		error: function( xhr ) {
		alert( 'Error: Request failed. Wantedpages' );
		}
	});
	
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'querypage',
			qppage: 'Wantedpages',
			qplimit: '5000',
			qpoffset: '3000',
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var results = data.query.querypage.results;
			iloop2: for (var i = 0; i < results.length; i++) {
				var pageObject = new WantedPage(results[i].title, results[i].value);
				for (var j = 0; j < wantedPages.length; j++) {
					if (wantedPages[j].title == pageObject.title) {
						continue iloop2; //don't put page into array
					}
				}
				wantedPages.push(pageObject);
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed. Wantedpages' );
		}
	});
	return wantedPages;
};

function filterWantedPages(wantedPages) {
	for (var i = 0; i < wantedPages.length; i++) {
		if ((wantedPages[i].title.indexOf("File:") == -1) && (wantedPages[i].title.indexOf("Template:") == -1)) { //not doing this for file or template pages
			$.ajax({
				url: apiUrl,
				data: {
					format: "json",
					action: 'query',
					list: "backlinks",
					bltitle: wantedPages[i].title,
					bllimit: 500,
					blnamespace: 0|4|6|8|10|12|14|3000|3002 //Main, Project (Factorio), File, MediaWiki, Template, Help, Category, Tutorial, Infobox
				},
				async: false,
				type: 'GET',
				success: function( data ) {
					if (data.query.backlinks.length == 0) {
						console.log("Removing " + wantedPages[i].title + " from the wantedPages.");
						wantedPages.splice(i, 1); 
					}
				},
				error: function( xhr ) {
					alert( 'Error: Backlinks request failed.' );
				}
			});
		}
	}
	return wantedPages;
};

function splitWantedPagesIntoDifferentLanguages(wantedPages) {
	var czechWantedPages = []; 
	var germanWantedPages = [];
	var spanishWantedPages = [];
	var frenchWantedPages = [];
	var italianWantedPages = [];
	var japaneseWantedPages = [];
	var dutchWantedPages = [];
	var polishWantedPages = [];
	var portugueseWantedPages = [];
	var russianWantedPages = [];
	var swedishWantedPages = [];
	var ukrainianWantedPages = [];
	var chineseWantedPages = [];
	var turkishWantedPages = [];
	var koreanWantedPages = [];
	var malayanWantedPages = [];
	var wantedFiles = [];
	var wantedFileTalk = [];
	var wantedTemplates = [];
	var otherWantedPages = [];

	for (var i = 0; i < wantedPages.length; i++) {
		switch (wantedPages[i].title.slice(-3)) {//"/cs", "/de", "/es", "/fr", "/it", "/ja", "/nl", "/pl", "/-br", "/ru", "/sv", "/uk", "/zh", "/tr", "/ko", "/ms"
			case "/cs": czechWantedPages.push(wantedPages[i]); break;
			case "/de": germanWantedPages.push(wantedPages[i]); break;
			case "/es": spanishWantedPages.push(wantedPages[i]); break;
			case "/fr": frenchWantedPages.push(wantedPages[i]); break;
			case "/it": italianWantedPages.push(wantedPages[i]); break;
			case "/ja": japaneseWantedPages.push(wantedPages[i]); break;
			case "/nl": dutchWantedPages.push(wantedPages[i]); break;
			case "/pl": polishWantedPages.push(wantedPages[i]); break;
			case "-br": portugueseWantedPages.push(wantedPages[i]); break;
			case "/ru": russianWantedPages.push(wantedPages[i]); break;
			case "/sv": swedishWantedPages.push(wantedPages[i]); break;
			case "/uk": ukrainianWantedPages.push(wantedPages[i]); break;
			case "/zh": chineseWantedPages.push(wantedPages[i]); break;
			case "/tr": turkishWantedPages.push(wantedPages[i]); break;
			case "/ko": koreanWantedPages.push(wantedPages[i]); break;
			case "/ms": malayanWantedPages.push(wantedPages[i]); break;
			default: if (wantedPages[i].title.slice(0, 5) == "File:") {wantedFiles.push(wantedPages[i])} else if (wantedPages[i].title.slice(0, 9) == "Template:") {wantedTemplates.push(wantedPages[i])} else if (wantedPages[i].title.slice(0, 10) == "File talk:") {wantedFileTalk.push(wantedPages[i])} else {otherWantedPages.push(wantedPages[i])}; break;
		}
	}
  
	getStubs();
	getDisambigs();
	
	createWantedPagesPage("cs", czechWantedPages, "Czech");
	createWantedPagesPage("de", germanWantedPages, "German");
	createWantedPagesPage("es", spanishWantedPages, "Spanish");
	createWantedPagesPage("fr", frenchWantedPages, "French");
	createWantedPagesPage("it", italianWantedPages, "Italian");
	createWantedPagesPage("ja", japaneseWantedPages, "Japanese");
	createWantedPagesPage("nl", dutchWantedPages, "Dutch");
	createWantedPagesPage("pl", polishWantedPages, "Polish");
	createWantedPagesPage("pt-br", portugueseWantedPages, "Portuguese");
	createWantedPagesPage("ru", russianWantedPages, "Russian");
	createWantedPagesPage("sv", swedishWantedPages, "Swedish");
	createWantedPagesPage("uk", ukrainianWantedPages, "Ukrainian");
	createWantedPagesPage("zh", chineseWantedPages, "Chinese");
	createWantedPagesPage("tr", turkishWantedPages, "Turkish");
	createWantedPagesPage("ko", koreanWantedPages, "Korean");
	createWantedPagesPage("ms", malayanWantedPages, "Malay");

	createWantedPagesPage("file", wantedFiles, "Files");
	createWantedPagesPage("file_talk", wantedFileTalk, "File talk");
	createWantedPagesPage("template", wantedTemplates, "Templates");
	createWantedPagesPage("other", otherWantedPages, "Other");
}

function createWantedPagesPage(location, wantedPages, language) {
	var languageSuffixes = ["cs", "de", "es", "fr", "it", "ja", "nl", "pl", "pt-br", "ru", "sv", "uk", "zh", "tr", "ko", "ms"]
	if (languageSuffixes.indexOf(location) > -1) {
		var formattedWantedPages = "Number of wanted pages in " + language + ": " + wantedPages.length + "\n{|class=wikitable\n!#\n!Page\n!Links to this page\n!Length of the corresponding English page in bytes";
		for (var i = 0; i < wantedPages.length; i++) {
			//I don't dare to make this into a function because I don't want this to be async so lets put a whole api request in here lul
			var enPageTitle = wantedPages[i].title.slice(0, - location.length - 1)
			var length = 0;
			if (enPageLength[enPageTitle]) {
				length = enPageLength[enPageTitle]
			} else {
				$.ajax({
					url: apiUrl,
					data: {
						format: 'json',
						action: 'query',
						titles: enPageTitle,
						prop: 'info',
					},
					async: false,
					dataType: 'json',
					type: 'POST',
					success: function( data ) {
						var pages = data.query.pages;
						var pageInfo = pages[Object.keys(pages)[0]];
						length = pageInfo['length'];
						if (!length) length = '---';
						var redirect = pageInfo['redirect'];
						if (redirect == "") {
							length = length + " (Redirect)";
						} else if (disambigs[enPageTitle]) {
							length = length + " (Disambiguation)";
						}
						if (stubs[enPageTitle]) {
							length = length + " (Stub)";
						}
						enPageLength[enPageTitle] = length
					},
					error: function( xhr ) {
						alert("Failed to get page length: " + enPageTitle);
					}
				});
			}
			formattedWantedPages = formattedWantedPages.concat("\n|-\n|" + (i + 1) + "\n|[https://wiki.factorio.com/index.php?title=" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].title + "]\n|[https://wiki.factorio.com/index.php?title=Special:WhatLinksHere/" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].value + "]\n|[https://wiki.factorio.com/index.php?title=" + encodeURI(enPageTitle) + " " + length + "]");
		}
	} else {
		var formattedWantedPages = "Number of wanted pages in " + language + ": " + wantedPages.length + "\n{|class=wikitable\n!#\n!Page\n!Links to this page";
		for (var i = 0; i < wantedPages.length; i++) {    
			formattedWantedPages = formattedWantedPages.concat("\n|-\n|" + (i + 1) + "\n|[https://wiki.factorio.com/index.php?title=" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].title + "]\n|[https://wiki.factorio.com/index.php?title=Special:WhatLinksHere/" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].value + "]");
		}
	}
	formattedWantedPages = formattedWantedPages.concat("\n|}");

	createPage(wantedPagesListsLocation + "/" + location, formattedWantedPages, "Updated the list of wanted pages for " + language + ".");
}

function compare(a,b) {
	if (parseInt(a.value) > parseInt(b.value))
		return -1;
	if (parseInt(a.value) < parseInt(b.value))
		return 1;
	if (a.title < b.title)
		return -1;
	if (a.title > b.title)
		return 1;
	return 0;
}

function WantedPage(pageTitle, pageValue) {
	this.title = pageTitle;
	this.value = pageValue;
}

/* Redirects -> Factorio:Redirects */

$("#create-redirect-list").click(function(){
	getToken();
	createRedirectList();
});

function createRedirectList() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	getRedirects();
};

function getRedirects() {
	var redirects = [];

	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'allpages',
			aplimit: '5000',
			apfilterredir: 'redirects',
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			redirects = data.query.allpages;
		},
		error: function( xhr ) {
			alert( 'Error: Allpages request failed.' );
		}
	});
  
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'allpages',
			aplimit: '5000',
			apfilterredir: 'redirects',
			apnamespace: '6'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			for (var i = 0; i < data.query.allpages.length; i++) {
				redirects.push(data.query.allpages[i])
			}
		},
		error: function( xhr ) {
			alert( 'Error: Allpages request failed.' );
		}
	});
  
	for (var i = 0; i < redirects.length; i++) {
		var backlinks = getBacklinks(redirects[i].title);
		if (redirects[i].title.search(/File:/i) == 0) {
			var imageusage = getFileUsage(redirects[i].title);
			//don't put imageusage into backlinks if it's already there:
			jloop1: for (var j = 0; j < imageusage.length; j++) {
				for (var k = 0; k < backlinks.length; k++) {
					if (backlinks[k].title == imageusage[j].title) {
						continue jloop1;
					}
				}
				backlinks.push(imageusage[j]);
			}
		}
		redirects[i].value = backlinks.length;  
	}
	redirects = redirects.sort(compare);
	createRedirectsPage("Factorio:Redirects", redirects);
};

function createRedirectsPage(loc, redirects) {
	var formattedRedirects = "{|class=wikitable\n!#\n!Redirect\n!Links to this redirect";
	for (var i = 0; i < redirects.length; i++) {    
		formattedRedirects = formattedRedirects.concat("\n|-\n|" + (i + 1) + "\n|[https://wiki.factorio.com/index.php?title=" + encodeURI(redirects[i].title) + "&redirect=no " + redirects[i].title + "]\n|[https://wiki.factorio.com/index.php?title=Special:WhatLinksHere/" + encodeURI(redirects[i].title) + " " + redirects[i].value + "]");
	}
	formattedRedirects = formattedRedirects.concat("\n|}");
	createPage(loc, formattedRedirects, "Updated the list of redirects.");
};

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

function getBacklinks(page) {
	var backlinks = [];
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'backlinks',
			bltitle: page,
			bllimit: 1000,
		},
		async: false,
		type: 'GET',
		success: function( data ) {
			backlinks = data.query.backlinks;
		},
		error: function( xhr ) {
			alert( 'Error: Backlinks request failed.' );
		}
	});
	return backlinks;
};

function getFileUsage(file) {
	var imageusage = [];
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'imageusage',
			iutitle: file,
			iulimit: 1000
		},
		async: false,
		type: 'GET',
		success: function( data ) {
			imageusage = data.query.imageusage;
		},
		error: function( xhr ) {
			alert( 'Error: Imageusage request failed.' );
		}
	});
	return imageusage;
};

//* General/generic functions *//

/* User is bot if userGroup.some(isBot) == true */

var userGroup = "";

function getUserGroup() {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			meta: 'userinfo',
			uiprop: 'groups',
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function(data) {
			userGroup = data.query.userinfo.groups
		},
	});
};

function isBot(group) {
	return group == "bot";
}

/* Get token of this session */

var globalToken;

function getToken() {
    $.ajax({
        url: apiUrl,
        data: {
            format: 'json',
            action: 'query',
            meta: 'tokens',
            bot: true
        },
        async: false,
        dataType: 'json',
        type: 'POST',
        success: function( data ) {
           globalToken = data.query.tokens.csrftoken;
        },
        error: function( xhr ) {
            console.log("Failed to get token.");
        }
    });
}


function genericEditPage(title, content, summary) {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'edit',
			title: title,
			text: content,
			token: globalToken,
			summary: summary,
			bot: true,
			nocreate: true
		},
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


function createPage(pageTitle, content, summary) {
    $.ajax({
        url: apiUrl,
        data: {
			format: 'json',
			action: 'edit',
			title: pageTitle,
			text: content,
			token: globalToken,
			summary: summary,
			bot: true
        },
        async: false,
        dataType: 'json',
        type: 'POST',
        success: function( data ) {
			console.log("Created page: " + pageTitle);
        },
        error: function( xhr ) {
			console.log("Failed to create page");
        }
    });
}

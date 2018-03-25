// ONLY CONTAINS SCRIPTS THAT I MADE, MODIFIED (WANTED PAGES), OR ONES MINE DEPEND ON (NAMELY CREATEPAGE, GETTOKEN AND COMPARE) //

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

/* Template:Inventory tooltips */

var lastTouchTime = 0;
document.addEventListener('touchstart', updateLastTouchTime, true);
function updateLastTouchTime() {
  lastTouchTime = new Date();
}

$(".tab-head").mousemove(function(e) {
  if (e.buttons > 0) return;
  if (new Date() - lastTouchTime < 500) return;
  var countCssRules = document.styleSheets[0].cssRules.length;
  var newRule = '.tab-head:hover:after{display: block; left: ' + (e.offsetX + 20) + 'px; top: ' + (e.offsetY + 20) + 'px;}';
  document.styleSheets[0].insertRule(newRule, countCssRules);
});

$(".tab .factorio-icon").mousemove(function(e) {
  if (e.buttons > 0) return;
  if (new Date() - lastTouchTime < 500) return;
  var countCssRules = document.styleSheets[0].cssRules.length;
  $(e.currentTarget).children("a").attr("title", "");
  var text = $(e.currentTarget).children("a").children("img").attr("alt");
  var newRule = '.tab .factorio-icon:hover:after{display: block; ' + "content: '" + text + "'}";
  document.styleSheets[0].insertRule(newRule, countCssRules);
});

/* Template:BlueprintString */

$(".bps-box").click(function(event) {
	var copyTarget = document.createElement("input");
	copyTarget.setAttribute("value", $( event.target ).children("p").html());
	document.body.appendChild(copyTarget);
	copyTarget.select();
	document.execCommand("copy");
	document.body.removeChild(copyTarget);
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
	console.log("Getting wantedPages...");
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
			qpoffset: '4000',
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
	
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'querypage',
			qppage: 'Wantedpages',
			qplimit: '5000',
			qpoffset: '8000',
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var results = data.query.querypage.results;
			iloop3: for (var i = 0; i < results.length; i++) {
				var pageObject = new WantedPage(results[i].title, results[i].value);
				for (var j = 0; j < wantedPages.length; j++) {
					if (wantedPages[j].title == pageObject.title) {
						continue iloop3; //don't put page into array
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
	var danishWantedPages = [];
	var hungarianWantedPages = [];
	var wantedFiles = [];
	var wantedFileTalk = [];
	var wantedTemplates = [];
	var otherWantedPages = [];

	for (var i = 0; i < wantedPages.length; i++) {
		switch (wantedPages[i].title.slice(-3)) {//"/cs", "/de", "/es", "/fr", "/it", "/ja", "/nl", "/pl", "/-br", "/ru", "/sv", "/uk", "/zh", "/tr", "/ko", "/ms", "/da", "/hu"
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
			case "/da": danishWantedPages.push(wantedPages[i]); break;
			case "/hu": hungarianWantedPages.push(wantedPages[i]); break;
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
	createWantedPagesPage("da", danishWantedPages, "Danish");
	createWantedPagesPage("hu", hungarianWantedPages, "Hungarian");

	createWantedPagesPage("file", wantedFiles, "Files");
	createWantedPagesPage("file_talk", wantedFileTalk, "File talk");
	createWantedPagesPage("template", wantedTemplates, "Templates");
	createWantedPagesPage("other", otherWantedPages, "Other");
}

function createWantedPagesPage(location, wantedPages, language) {
	var languageSuffixes = ["cs", "de", "es", "fr", "it", "ja", "nl", "pl", "pt-br", "ru", "sv", "uk", "zh", "tr", "ko", "ms", "da", "hu"]
	if (languageSuffixes.indexOf(location) > -1) {
		var formattedWantedPages = "Number of wanted pages in " + language + ": " + wantedPages.length + "\n{|class=wikitable\n!#\n!Page\n!Links to this page\n!Length of the corresponding English page in bytes";
		for (var i = 0; i < wantedPages.length; i++) {
			//I don't dare to make this into a function because I don't want this to be async so lets put a whole api request in here lul
			var enPageTitle = wantedPages[i].title.slice(0, - location.length - 1)
			var length = 0;
			if (enPageTitle == "") {
				length = '---';
			} else if (enPageLength[enPageTitle]) {
				length = enPageLength[enPageTitle];
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
			formattedWantedPages = formattedWantedPages.concat("\n|-\n|" + (i + 1) + "\n|[" + mw.config.get('wgServer') + "/index.php?title=" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].title + "]\n|[" + mw.config.get('wgServer') + "/index.php?title=Special:WhatLinksHere/" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].value + "]\n|[" + mw.config.get('wgServer') + "/index.php?title=" + encodeURI(enPageTitle) + " " + length + "]");
		}
	} else {
		var formattedWantedPages = "Number of wanted pages in " + language + ": " + wantedPages.length + "\n{|class=wikitable\n!#\n!Page\n!Links to this page";
		for (var i = 0; i < wantedPages.length; i++) {    
			formattedWantedPages = formattedWantedPages.concat("\n|-\n|" + (i + 1) + "\n|[" + mw.config.get('wgServer') + "/index.php?title=" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].title + "]\n|[" + mw.config.get('wgServer') + "/index.php?title=Special:WhatLinksHere/" + encodeURI(wantedPages[i].title) + " " + wantedPages[i].value + "]");
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

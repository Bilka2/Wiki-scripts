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

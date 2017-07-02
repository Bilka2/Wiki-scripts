/* on MediaWiki:Common.js */

/* Script in here will be executed when the page is "ready" */
$(document).ready(getNumberOfActiveUsers);

/* show correct number of active users on the main page */

function getNumberOfActiveUsers() {
	if (document.getElementById("active-users")) {
		$.ajax({
			url: 'https://wiki.factorio.com/api.php',
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


/* on User:BilkaBot/Other.js */

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
		url: 'https://wiki.factorio.com/api.php',
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

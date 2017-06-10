/* User is bot if userGroup.some(isBot) == true */

var userGroup = "";

function getUserGroup() {
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
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


var globalToken;

function getToken() {
    $.ajax({
        url: 'https://wiki.factorio.com/api.php',
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
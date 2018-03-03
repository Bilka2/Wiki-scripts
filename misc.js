// Deleting redirects. Get array of full page names -> delete all pages in array. Is run manually by pasting the array and the loop into the console //
function deleteRedirect(title) {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'delete',
			title: title,
			reason: 'Unused/unneeded/redundant redirect.',
			token: globalToken
		},
		dataType: 'json',
		type: 'POST',
		success: function( data ) {
			console.log("Deleted " + title);
		},
		error: function( xhr ) {
			alert("Failed to delete " + title);
		}
	});
}

var array = ["File:Tanks.png", "File:Toolbelt.png"]; //this is an example

for (var i = 0; i < array.length; i++) {
	deleteRedirect(array[i])
}
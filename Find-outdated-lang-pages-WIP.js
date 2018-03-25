var languages = {
	{suffix:"cs", name:"Czech"},
	{suffix:"de", name:"German"},
	{suffix:"es", name:"Spanish"},
	{suffix:"fr", name:"French"},
	{suffix:"it", name:"Italian"},
	{suffix:"ja", name:"Japanese"},
	{suffix:"nl", name:"Dutch"},
	{suffix:"pl", name:"Polish"},
	{suffix:"pt-br", name:"Portuguese"},
	{suffix:"ru", name:"Russian"},
	{suffix:"sv", name:"Swedish"},
	{suffix:"uk", name:"Ukrainian"},
	{suffix:"zh", name:"Chinese"},
	{suffix:"tr", name:"Turkish"},
	{suffix:"ko", name:"Korean"},
	{suffix:"ms", name:"Malay"},
	{suffix:"da", name:"Danish"},
	{suffix:"hu", name:"Hungarian"}
};

function main(languages) {
	var englishPages = getCategorymembers('Category:English page');
	//getPageRevisions(englishPages, false);
	var englishPagesRevisions = getLastEditDateByPageArray(englishPages.join('|'));
	for (var i = 0; i < languages.length; i++) {
		var langPages = getCategorymembers('Category:' + languages[i].name + ' page');
		var langPagesRevisions = getLastEditDateByPageArray(langPages.join('|'));
	}
};

function getCategorymembers(category) {
	var array = [];
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			list: 'categorymembers',
			cmtitle: category,
			cmlimit: 1000,
			cmprop: 'title'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var categorymembers = data.query.categorymembers;
			console.log('Found ' + categorymembers.length + ' pages in ' + category);
			for (var i = 0; i < categorymembers.length; i++) {
				array.push(categorymembers[i].title);
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
	return array;
};

function getPageRevisions(array, removeRevisionsByBilka) {
	var pageRevisions = getPageRevisionsByPages(array.join('|'));
	if (removeRevisionsByBilka) {
		for (var i = 0; i < pageRevisions.length; i++) {
			var rev = getLatestRevisionNotByBilka(pageRevisions[i]);
			if (rev !== pageRevisions[i]) {
				//here
			}
		}
	}
};

function getLatestRevisionNotByBilka(pageRevisions) {
	var revisions = pageRevisions;
	while (revisions.user.includes("Bilka") && revisions.parentid != 0) {
		revisions = getPageRevisionsByRevID(revisions.parentid);
	}
	return revisions;
};

function getPageRevisionsByPages(pages) {
	var array = [];
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			prop: 'revisions',
			titles: pages,
			rvprop: 'timestamp|user|ids'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			for (var i = 0; i < pages.length; i++) {
				if (pages[i].missing) continue;
				var pageRevisions = new pageRevisions(pages[i].title, pages[i].revisions[0].user, pages[i].revisions[0].timestamp, pages[i].revisions[0].revid, pages[i].revisions[0].parentid);
				array.push(pageRevisions);
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
	return array;
};

function getPageRevisionsByRevID(revid) {
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			prop: 'revisions',
			revids: revid,
			rvprop: 'timestamp|user|ids'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var pageInfo = pages[Object.keys(pages)[0]];
			var pageRevisions = new pageRevisions(pageInfo.title, pageInfo.revisions[0].user, pageInfo.revisions[0].timestamp, pageInfo.revisions[0].revid, pageInfo.revisions[0].parentid);
			return pageRevisions;
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
};


function pageRevisions(title, user, timestamp, revid, parentid) {
  this.title = title;
  this.user = user;
  this.timestamp = timestamp;
  this.revid = revid;
  this.parentid = parentid;
}

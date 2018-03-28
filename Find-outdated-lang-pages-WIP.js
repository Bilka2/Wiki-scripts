var languages = [
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
];

function main(languages) {
	var englishPages = getCategorymembers('Category:English page');
	var englishPagesRevisions = getPageRevisions(englishPages, false);
	var langPages = {};
	for (var i = 0; i < languages.length; i++) {
		var pages = getCategorymembers('Category:' + languages[i].name + ' page');
		var pagesRevisions = getPageRevisions(langPages, true);
		langPages[languages[i].suffix] = {pages: pages, pagesRevisions: pagesRevisions, name: languages[i].name};
	}
	for (var key in langPages) {
		if (!langPages.hasOwnProperty(key)) continue;
		var value = langPages[key];
		//here
	}
};

function test() {
	var englishPages = getCategorymembers('Category:English page');
	var englishPagesRevisions = getPageRevisions(englishPages, false);
	console.log(englishPages);
	console.log(englishPagesRevisions);
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
			categorymembers.forEach(function(page){
				array.push(page.title)
			});
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
	return array;
};

function getPageRevisions(array, removeRevisionsByBilka) {
	var pageRevisions = staggerGetPageRevisionsByPages(array); //We timeout or something if we query too many pages
	if (removeRevisionsByBilka) {
		for (var i = 0; i < pageRevisions.length; i++) pageRevisions[i] = getLatestRevisionNotByBilka(pageRevisions[i]);
	}
	return pageRevisions;
};

function staggerGetPageRevisionsByPages(array) {
	var resultArray = [];
	for (var i = 0; i < array.length; i += 200) {
		var arrayPart = array.slice(i, i + 200);
		if (i == 0) resultArray = getPageRevisionsByPages(arrayPart.join('|'));
		else resultArray = resultArray.concat(getPageRevisionsByPages(arrayPart.join('|')));
	}
	return resultArray;
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
			for (var key in pages) {
				if (!pages.hasOwnProperty(key)) continue;
				var page = pages[key];
				if (page.missing) continue;
				var pageRevisions = pageRevisionsFromAPIResponse(page);
				array.push(pageRevisions);
			}
		},
		error: function( xhr ) {
			alert( 'Error: Request failed. ' + xhr.status + ': ' + xhr.statusText);
		}
	});
	return array;
};

function getLatestRevisionNotByBilka(pageRevisions) {
	var revisions = pageRevisions;
	while (revisions.user.includes("Bilka") && revisions.parentid != 0) {
		revisions = getPageRevisionsByRevID(revisions.parentid);
	}
	return revisions;
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
			var pageRevisions = pageRevisionsFromAPIResponse(pageInfo);
			return pageRevisions;
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
};

function pageRevisionsFromAPIResponse(page) {
	return new pageRevisions(page.title, page.revisions[0].user, page.revisions[0].timestamp, page.revisions[0].revid, page.revisions[0].parentid);
};

function pageRevisions(title, user, timestamp, revid, parentid) {
  this.title = title;
  this.user = user;
  this.timestamp = timestamp;
  this.revid = revid;
  this.parentid = parentid;
};

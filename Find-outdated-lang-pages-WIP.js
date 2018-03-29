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
	var englishPagesRevisions = getPageRevisions(getCategorymembers('Category:English page'), false);
	var langPages = {};
	for (var i = 0; i < /*languages.length*/ 1 ; i++) {
		var pagesRevisions = getPageRevisions(getCategorymembers('Category:' + languages[i].name + ' page'), true);
		langPages[languages[i].suffix] = {pagesRevisions: pagesRevisions, name: languages[i].name};
	}
	for (var suffix in langPages) {
		if (!langPages.hasOwnProperty(suffix)) continue;
		var value = langPages[suffix];
		var langPageRevisionsList = value.pagesRevisions;
		for (var langPageName in langPageRevisionsList) {
			if (!langPageRevisionsList.hasOwnProperty(langPageName)) continue;
			var langPageRevisions = langPageRevisionsList[langPageName];
			isLangPageOutdated(langPageRevisions, suffix, englishPagesRevisions);
			//put in array/object
			//print outdated pages
		}
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
	var pageRevisionsList = staggerGetPageRevisionsByPages(array); //We timeout or something if we query too many pages
	if (removeRevisionsByBilka) {
		for (var i = 0; i < pageRevisionsList.length; i++) pageRevisionsList[i] = getLatestRevisionNotByBilka(pageRevisionsList[i]);
	}
	//turn array into object indexed by page name to make it easier to find the properties of a page
	var pageRevisionsObject = {};
	pageRevisionsList.forEach(function(pageRevisions) {
		pageRevisionsObject[pageRevisions.title] = pageRevisions;
	});
	return pageRevisionsObject;
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
	var pageRevisions;
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
			pageRevisions = pageRevisionsFromAPIResponse(pageInfo);
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
	return pageRevisions;
};

function isLangPageOutdated(langPageRevisions, suffix, englishPagesRevisions) {
	var langTimestamp = langPageRevisions.timestamp;
	var en = getEnglishPageRevisions(langPageRevisions.title, suffix, englishPagesRevisions);
	if (!en) {
		console.log('No page ' + getEnglishPageName(langPageRevisions.title, suffix))
		return true; // Outdated	
	}
	/*console.log('en: ' + en.timestamp + ', ' + suffix + ': ' + langTimestamp);
	if (en.timestamp < langTimestamp) console.log('en.timestamp < langTimestamp ' + langPageRevisions.title);
	if (en.timestamp > langTimestamp) console.log('en.timestamp > langTimestamp ' + langPageRevisions.title);*/
	if (en.timestamp > langTimestamp) return true;
	return false;
};

function getEnglishPageRevisions(langPageName, suffix, englishPagesRevisions) {
	return englishPagesRevisions[getEnglishPageName(langPageName, suffix)];
};

function getEnglishPageName(langPageName, suffix) {
	return langPageName.slice(0, - suffix.length - 1);
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

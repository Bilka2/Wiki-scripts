/* Infobox updating */

var noInfobox = ["Basic oil processing", "Advanced oil processing", "Coal liquefaction", "Empty barrel", "Heavy oil cracking", "Light oil cracking", "Solid fuel from heavy oil", "Solid fuel from light oil", "Solid fuel from petroleum gas", "Water barrel", "Crude oil barrel", "Heavy oil barrel", "Sulfuric acid barrel", "Light oil barrel", "Petroleum gas barrel", "Lubricant barrel", "Empty crude oil barrel", "Empty heavy oil barrel", "Empty light oil barrel", "Empty lubricant barrel", "Empty petroleum gas barrel", "Empty sulfuric acid barrel", "Empty water barrel", "Fill crude oil barrel", "Fill heavy oil barrel", "Fill light oil barrel", "Fill lubricant barrel", "Fill petroleum gas barrel", "Fill sulfuric acid barrel", "Fill water barrel"]
var version = "0.15.37";


var para = "";
function getInputPara(item, search, length, name, itemName) {
	var paraStart = item.search(search) + length; //finds the beginning of the para, is after para-name
	if (paraStart < length) {
		console.log(itemName + ": No " + name + " found.");
		para = "";
	} else {
		var paraCut = item.slice(paraStart);  //lets the string begin after the parameter name
		var paraEnd = paraCut.search(/\||}}/); //finds the end of the parameter definition
		para = paraEnd < 1 ? paraCut : paraCut.slice(0, paraEnd); //para ends at para-end if it exists
	}
	return para;
};


var pagePara = "";
function getOldPara(content, pageParaStart, length, name, itemName) {
	if (pageParaStart < length) { //if the start is less than the length of the para name (name) then the search was unsuccessful
		console.log(itemName + ": No " + name + " found on page.");
		pagePara = "";
	} else {
		var pageParaCut = content.slice(pageParaStart);
		pageParaStart = pageParaCut.search(/\w/);
		pageParaCut = pageParaCut.slice(pageParaStart); //removes anything before the parameter that does not belong there, like = and \s
		var pageParaEnd = pageParaCut.search(/\||}}/); //finds the end of the parameter definition
		pagePara = pageParaEnd < 1 ? pageParaCut : pageParaCut.slice(0, pageParaEnd); //pagePara ends at para-end if it exists
	}
	return pagePara;
};

var summary = "";
var newContent = "";
function updatePara(content, para, pagePara, name, newPageParaStart, length, itemName) {  //also needs version, summary, changes newContent and summary
	if (pagePara.length > 0) {
		var newPageParaCut = content.slice(newPageParaStart); //lets the string being after the parameter name
		var newPageParaEnd = newPageParaCut.search(/\||}}/) + newPageParaStart; //finds the end of the parameter definition, with added parastart so that it's relative to the start of the entire string, not the parameter string
		if (para.length > 0) {
			newContent = content.slice(0, newPageParaStart) + " = " + para + "\n" + content.slice(newPageParaEnd);
			console.log("Replaced " + itemName + " " + name + ".");
			summary = summary + "Updated " + name + " to " + version + ". ";
		} else {
			newPageParaStart = newPageParaStart - length; //makes it so that the start of the para string if before the name, so that the name also gets deleted
			newContent = content.slice(0, newPageParaStart) + content.slice(newPageParaEnd); //removes what is between parastart and paraend from newcontent
			console.log("Removed " + itemName + " " + name + ". ");
			summary = summary + "Removed " + name + ". ";
		}
	} else if (para.length > 0) {
		var InfoboxStart = content.search(/{{Infobox/i) + 9; //finds the start of the infobox, excludes {{infobox from the resulting string
		newContent = content.slice(0, InfoboxStart) + "\n|" + name + " = " + para + content.slice(InfoboxStart);
		console.log("Added " + itemName + " " + name + ". ");
		summary = summary + "Added " + name + ". ";
	}
};


function editPage(title, itemName) { //also uses summary, globalToken, newContent
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'edit',
			title: title,
			text: newContent,
			token: globalToken,
			summary: summary,
			bot: true,
			nocreate: true
		},
		dataType: 'json',
		type: 'POST',
		success: function( data ) {
			console.log("Updated " + itemName);
		},
		error: function( xhr ) {
			console.log("Failed to update " + itemName);
		}
	});
};


$("#RecipeUpdate").click(function(){
    getRecipes();
});

function getRecipes() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	var recipeInput = prompt("Please enter the recipes");
	if (recipeInput != null) {
		getToken();
		var items = recipeInput.split(/\s\s/g);
		console.log(items.length + " items detected");
		items.forEach(removeDuplicateRecipesAndUpdateInfobox);
	}
};


function removeDuplicateRecipesAndUpdateInfobox(recipes) {
	var itemNameEnd = recipes.search("\\|");
	var itemName = recipes.slice(0, itemNameEnd).trim();
	
	//Remove Itemnames if the item does not have a page on the wiki, so that the item is removed from the output
	noInfobox.forEach(function(infoboxName) {
	if (itemName == infoboxName) {
		console.log("Removed " + itemName + " from output.");
		itemName = "";
	}
	})
	if (itemName.length == 0) {
		return;
	}
	
	var recipe = getInputPara(recipes, "\\|recipe = ", 10, "recipe", itemName).trim();
	var totalRaw = getInputPara(recipes, "\\|total-raw = ", 13, "total-raw", itemName).trim();
	var expRecipe = getInputPara(recipes, "\\|expensive-recipe = ", 20, "expensive-recipe", itemName).trim();
	var expTotalRaw = getInputPara(recipes, "\\|expensive-total-raw = ", 23, "expensive-total-raw", itemName).trim();	
	
	//remove duplicate recipes, but only if the recipe actually exists
	if ((expTotalRaw == expRecipe) && (expTotalRaw.length > 0)) {
		expTotalRaw = "";
		console.log(itemName + ": Removed expensive-total-raw because it was a duplicate of expensive-recipe.");
	} else if ((expTotalRaw == totalRaw) && (expTotalRaw.length > 0)) {
		expTotalRaw = "";
		console.log(itemName + ": Removed expensive-total-raw because it was a duplicate of total-raw.");
	}
	if ((expRecipe == recipe) && (expRecipe.length > 0)) {
		expRecipe = "";
		console.log(itemName + ": Removed expensive-recipe because it was a duplicate of recipe.");
	}
	if ((totalRaw == recipe) && (totalRaw.length > 0)) {
		totalRaw = "";
		console.log(itemName + ": Removed total-raw because it was a duplicate of recipe.");
	}
	
	
	//get page content of the item -> oldContent
	var oldContent = "";
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: 'Infobox:' + itemName,
			prop: 'revisions',
			rvprop: 'content'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var revisions = pages[Object.keys(pages)[0]].revisions[0];
			oldContent = revisions[Object.keys(revisions)[2]];
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
			oldContent = "";
		}
	});
	if (oldContent.length = 0) {
		console.log("No " + itemName + " page found.");
		return;
	}
	
	
	//find recipes in page (oldContent)
	var match = oldContent.match(/\|\s*recipe/);
	var recipeLength = match == null ? 0 : match.toString().length; //var value = *condition* ? *true* : *false*;
	var pageRecipeStart = oldContent.search(/\|\s*recipe/) + recipeLength; //so that it doesn't find "|prototype-type = recipe"
	var pageRecipe = getOldPara(oldContent, pageRecipeStart, recipeLength, "recipe", itemName).trim();

	var pageTotalRawStart = oldContent.search(/(\s|\|)total-raw/) + 10;
	var pageTotalRaw = getOldPara(oldContent, pageTotalRawStart, 10, "total-raw", itemName).trim();
	
	var pageExpRecipeStart = oldContent.search(/(\s|\|)expensive-recipe/) + 17;
	var pageExpRecipe = getOldPara(oldContent, pageExpRecipeStart, 17, "expensive-recipe", itemName).trim();

	var pageExpTotalRawStart = oldContent.search(/(\s|\|)expensive-total-raw/) + 20;
	var pageExpTotalRaw = getOldPara(oldContent, pageExpTotalRawStart, 20, "expensive-total-raw", itemName).trim();
	
	summary = "";
	
	//change page if anything is different (this INCLUDES different formatting)
	newContent = "";
	if ((pageRecipe == recipe) && (pageTotalRaw == totalRaw) && (pageExpRecipe == expRecipe) && (pageExpTotalRaw == expTotalRaw)) {
		console.log(itemName + " page was not changed.")
	} else {
		if (pageRecipe != recipe) {
			newContent = oldContent;
			var newPageRecipeStart = newContent.search(/(\s|\|)recipe/) + 7;
			updatePara(newContent, recipe, pageRecipe, "recipe", newPageRecipeStart, 7, itemName);
		}
		if (pageTotalRaw != totalRaw) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageTotalRawStart = newContent.search(/(\s|\|)total-raw/) + 10;
			updatePara(newContent, totalRaw, pageTotalRaw, "total-raw", newPageTotalRawStart, 10, itemName);
		}
		if (pageExpRecipe != expRecipe) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageExpRecipeStart = newContent.search(/(\s|\|)expensive-recipe/) + 17;
			updatePara(newContent, expRecipe, pageExpRecipe, "expensive-recipe", newPageExpRecipeStart, 17, itemName);
		}
		if (pageExpTotalRaw != expTotalRaw) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageExpTotalRawStart = newContent.search(/(\s|\|)expensive-total-raw/) + 20;
			updatePara(newContent, expTotalRaw, pageExpTotalRaw, "expensive-total-raw", newPageExpTotalRawStart, 20, itemName);
		}
	}
	//alright, newContent should be defined, change page:
	if (newContent.length > 0) editPage("Infobox:" + itemName, itemName);	
}

$("#ItemUpdate").click(function(){
    getItems();
});

function getItems() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	var itemInput = prompt("Please enter the consumers, stack-sizes and required-technologies");
	if (itemInput != null) {
		getToken();
		var items = itemInput.split(/\s\s/g);
		console.log(items.length + " items detected");
		items.forEach(updateItemInfoboxes);
	}
};

function updateItemInfoboxes(item) {
	var itemNameEnd = item.search("\\|");
	var itemName = item.slice(0, itemNameEnd).trim();
	
	//Remove items that don't have Infoboxes on the wiki
	noInfobox.forEach(function(infoboxName) {
	if (itemName == infoboxName) {
		console.log("Removed " + itemName + " from output.");
		itemName = "";
	}
	})
	if (itemName.length == 0) return;
	
	var consumers = getInputPara(item, "\\|consumers = ", 13, "consumers", itemName).trim();
	var stackSize = getInputPara(item, "\\|stack-size = ", 14, "stack-size", itemName).trim();
	var reqTech = getInputPara(item, "\\|required-technologies = ", 25, "required-technologies", itemName).trim();	
	
	//get page content of the item -> oldContent
	var oldContent = "";
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: 'Infobox:' + itemName,
			prop: 'revisions',
			rvprop: 'content'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var revisions = pages[Object.keys(pages)[0]].revisions[0];
			oldContent = revisions[Object.keys(revisions)[2]];
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
			oldContent = "";
		}
	});
	if (oldContent.length = 0) {
		console.log("No " + itemName + " page found.");
		return;
	}
	
	//find recipes in page (oldContent)
	var pageConsumersStart = oldContent.search(/(\s|\|)consumers/) + 10;
	var pageConsumers = getOldPara(oldContent, pageConsumersStart, 10, "consumers", itemName).trim();
	
	var pageStackSizeStart = oldContent.search(/(\s|\|)stack-size/) + 11;
	var pageStackSize = getOldPara(oldContent, pageStackSizeStart, 11, "stack-size", itemName).trim();
	
	var pageReqTechStart = oldContent.search(/(\s|\|)required-technologies/) + 22;
	var pageReqTech = getOldPara(oldContent, pageReqTechStart, 22, "required-technologies", itemName).trim();
	
	
	summary = "";
	newContent = "";
	if ((pageConsumers == consumers) && (pageStackSize == stackSize) && (pageReqTech == reqTech)) {
		console.log(itemName + " page was not changed.")
	} else {
		if (pageConsumers != consumers) {
			newContent = oldContent;
			var newPageConsumersStart = newContent.search(/(\s|\|)consumers/) + 10;
			updatePara(newContent, consumers, pageConsumers, "consumers", newPageConsumersStart, 10, itemName);
		}
		if (pageStackSize != stackSize) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageStackSizeStart = newContent.search(/(\s|\|)stack-size/) + 11;
			updatePara(newContent, stackSize, pageStackSize, "stack-size", newPageStackSizeStart, 11, itemName);
		}
		if (pageReqTech != reqTech) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageReqTechStart = newContent.search(/(\s|\|)required-technologies/) + 22;
			updatePara(newContent, reqTech, pageReqTech, "required-technologies", newPageReqTechStart, 22, itemName);
		}
	}
	
	//alright, newContent should be defined, change page:
	if (newContent.length > 0) editPage("Infobox:" + itemName, itemName);
}

$("#TechUpdate").click(function(){
    getTechnologies();
});

function getTechnologies() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	var techInput = prompt("Please enter the technologies");
	if (techInput != null) {
		getToken();
		var techs = techInput.split(/\s\s/g);
		console.log(techs.length + " techs detected");
		techs.forEach(updateTechnologyInfobox);
	}
}

function updateTechnologyInfobox(tech) {
	var techNameEnd = tech.search("\\|");
	var techName = tech.slice(0, techNameEnd).trim();
	
	
	var cost = getInputPara(tech, "\\|cost = ", 8, "cost", techName).trim();
	var costMulti = getInputPara(tech, "\\|cost-multiplier = ", 19, "cost-multiplier", techName).trim();
	var expCostMulti = getInputPara(tech, "\\|expensive-cost-multiplier = ", 29, "expensive-cost-multiplier", techName).trim();
	var reqTech = getInputPara(tech, "\\|required-technologies = ", 25, "required-technologies", techName).trim();
	var allows = getInputPara(tech, "\\|allows = ", 10, "allows", techName).trim();
	var effects = getInputPara(tech, "\\|effects = ", 11, "effects", techName).trim();
	
	
	//get page content of the tech -> oldContent
	var oldContent = "";
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: 'Infobox:' + techName + ' (research)',
			prop: 'revisions',
			rvprop: 'content'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var revisions = pages[Object.keys(pages)[0]].revisions[0];
			oldContent = revisions[Object.keys(revisions)[2]];
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
			oldContent = "";
		}
	});
	if (oldContent.length = 0) {
		console.log("No " + techName + " page found.");
		return;
	}
	
	
	//find costs etc in page (oldContent)
	var pageCostStart = oldContent.search(/(\s|\|)cost(\s|=)/) + 6;
	var pageCost = getOldPara(oldContent, pageCostStart, 6, "cost", techName).trim();
	
	var pageCostMultiStart = oldContent.search(/(\s|\|)cost-multiplier/) + 16;
	var pageCostMulti = getOldPara(oldContent, pageCostMultiStart, 16, "cost-multiplier", techName).trim();
	
	var pageExpCostMultiStart = oldContent.search(/(\s|\|)expensive-cost-multiplier/) + 26;
	var pageExpCostMulti = getOldPara(oldContent, pageExpCostMultiStart, 26, "expensive-cost-multiplier", techName).trim();
	
	var pageReqTechStart = oldContent.search(/(\s|\|)required-technologies/) + 22;
	var pageReqTech = getOldPara(oldContent, pageReqTechStart, 22, "required-technologies", techName).trim();
	
	var pageAllowsStart = oldContent.search(/(\s|\|)allows/) + 7;
	var pageAllows = getOldPara(oldContent, pageAllowsStart, 7, "allows", techName).trim();
	
	var pageEffectsStart = oldContent.search(/(\s|\|)effects/) + 8;
	var pageEffects = getOldPara(oldContent, pageEffectsStart, 8, "effects", techName).trim();
	
	
	summary = "";
	newContent = "";
	
	//change page if anything is different (this INCLUDES different formatting)
	if ((pageCost == cost) && (pageCostMulti == costMulti) && (pageExpCostMulti == expCostMulti) && (pageReqTech == reqTech) && (pageAllows == allows) && (pageEffects == effects)) {
		console.log(techName + " page was not changed.")
	} else {
		if (pageCost != cost) {
			newContent = oldContent;
			var newPageCostStart = newContent.search(/(\s|\|)cost(\s|=)/) + 6;
			updatePara(newContent, cost, pageCost, "cost", newPageCostStart, 6, techName);
		}
		if (pageCostMulti != costMulti) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageCostMultiStart = newContent.search(/(\s|\|)cost-multiplier/) + 16;
			updatePara(newContent, costMulti, pageCostMulti, "cost-multiplier", newPageCostMultiStart, 16, techName);
		}
		if (pageExpCostMulti != expCostMulti) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageExpCostMultiStart = newContent.search(/(\s|\|)expensive-cost-multiplier/) + 26;
			updatePara(newContent, expCostMulti, pageExpCostMulti, "expensive-cost-multiplier", newPageExpCostMultiStart, 26, techName);
		}
		if (pageReqTech != reqTech) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageReqTechStart = newContent.search(/(\s|\|)required-technologies/) + 22;
			updatePara(newContent, reqTech, pageReqTech, "required-technologies", newPageReqTechStart, 22, techName);
		}
		if (pageAllows != allows) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageAllowsStart = newContent.search(/(\s|\|)allows/) + 7;
			updatePara(newContent, allows, pageAllows, "allows", newPageAllowsStart, 7, techName);
		}
		if (pageEffects != effects) {
			if (newContent.length == 0) newContent = oldContent;
			var newPageEffectsStart = newContent.search(/(\s|\|)effects/) + 8;
			updatePara(newContent, effects, pageEffects, "effects", newPageEffectsStart, 8, techName);
		}	
	}
	//alright, newContent should be defined, change page:
	if (newContent.length > 0) editPage("Infobox:" + techName + " (research)", techName);	
}

$("#AllUpdate").click(function(){
    getAll();
});

function getAll() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	getToken();
	newVersion = prompt("Please enter the new version.");
	if (newVersion != null) version = newVersion.trim();
	var recipeInput = prompt("Please enter the recipes.");
	var itemInput = prompt("Please enter the consumers, stack-sizes and required-technologies.");
	var techInput = prompt("Please enter the technologies.");
	
	if (recipeInput != null) {
		var recipeArray = recipeInput.split(/\s\s/g);
		console.log(recipeArray.length + " recipes detected");
		recipeArray.forEach(removeDuplicateRecipesAndUpdateInfobox);
	}
	if (itemInput != null) {
		var items = itemInput.split(/\s\s/g);
		console.log(items.length + " items detected");
		items.forEach(updateItemInfoboxes);
	}
	if (techInput != null) {
		var techs = techInput.split(/\s\s/g);
		console.log(techs.length + " techs detected");
		techs.forEach(updateTechnologyInfobox);
	}
}

$("#TechDataUpdate").click(function(){
    getTechData();
});

function getTechData() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	var techInput = prompt("Please enter the technology internal-names.");
	if (techInput != null) {
		getToken();
		var techs = techInput.split(/\s\s/g);
		console.log(techs.length + " techs detected");
		techs.forEach(updateTechnologyDataInfobox);
	}
}

function updateTechnologyDataInfobox(tech) {
	var techNameEnd = tech.search("\\|");
	var techName = tech.slice(0, techNameEnd).trim();
	
	var internalName = getInputPara(tech, "\\|internal-name = ", 17, "internal-name", techName).trim();
	var prototypeType = "technology";
	
	//get page content of the tech -> oldContent
	var oldContent = "";
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: 'Infobox:' + techName + ' (research)',
			prop: 'revisions',
			rvprop: 'content'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var revisions = pages[Object.keys(pages)[0]].revisions[0];
			oldContent = revisions[Object.keys(revisions)[2]];
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
			oldContent = "";
		}
	});
	if (oldContent.length = 0) {
		console.log("No " + techName + " page found.");
		return;
	}
	
	var pageInternalNameStart = oldContent.search(/(\s|\|)internal-name/) + 14;
	var pageInternalName = getOldPara(oldContent, pageInternalNameStart, 14, "internal-name", techName).trim();
	
	var pagePrototypeTypeStart = oldContent.search(/(\s|\|)prototype-type/) + 15;
	var pagePrototypeType = getOldPara(oldContent, pagePrototypeTypeStart, 15, "prototype-type", techName).trim();
	
	summary = "";
	newContent = "";
	if ((pageInternalName == internalName) && (pagePrototypeType == prototypeType)) {
		console.log(techName + " page was not changed.")
	} else {
		if (pageInternalName != internalName) {
			newContent = oldContent;
			var newInternalNameStart = newContent.search(/(\s|\|)internal-name/) + 14;
			updatePara(newContent, internalName, pageInternalName, "internal-name", newInternalNameStart, 14, techName);
		}
		if (pagePrototypeType != prototypeType) {
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPrototypeTypeStart = newContent.search(/(\s|\|)prototype-type/) + 15;
			updatePara(newContent, prototypeType, pagePrototypeType, "prototype-type", newPrototypeTypeStart, 15, techName);
		}
	}
	
	//alright, newContent should be defined, change page:
	if (newContent.length > 0) {
		editPage("Infobox:" + techName + " (research)", techName);
	}
}

$("#ProtypeTypeAndItemInternalNameUpdate").click(function(){
    getProtypeTypesAndItemInternalNames();
});

function getProtypeTypesAndItemInternalNames() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	var typeAndNameInput = prompt("Please enter the prototype-type and internal-name of everything except technologies.");
	if (typeAndNameInput != null) {
		getToken();
		var typesAndNames = typeAndNameInput.split(/\s\s/g);
		console.log(typesAndNames.length + " types and names detected");
		typesAndNames.forEach(updateProtypeTypeAndInternalNameInItemInfobox);
	}
}

function updateProtypeTypeAndInternalNameInItemInfobox(typeAndName) {
	var itemNameEnd = typeAndName.search("\\|");
	var itemName = typeAndName.slice(0, itemNameEnd).trim();
	
	//Remove items that don't have Infoboxes on the wiki
	noInfobox.forEach(function(infoboxName) {
		if (itemName == infoboxName) {
			console.log("Removed " + itemName + " from output.");
			itemName = "";
		}
	})
	if (itemName.length == 0) return;
	
	var prototypeType = getInputPara(typeAndName, "\\|prototype-type = ", 18, "prototype-type", itemName).trim();
	var internalName = getInputPara(typeAndName, "\\|internal-name = ", 17, "internal-name", itemName).trim();
	
	//get page content of the item -> oldContent
	var oldContent = "";
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: 'Infobox:' + itemName,
			prop: 'revisions',
			rvprop: 'content'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var revisions = pages[Object.keys(pages)[0]].revisions[0];
			oldContent = revisions[Object.keys(revisions)[2]];
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
		}
	});
	if (oldContent.length = 0) {
		console.log("No " + itemName + " page found.");
		return;
	}
	
	var pagePrototypeTypeStart = oldContent.search(/(\s|\|)prototype-type/) + 15;
	var pagePrototypeType = getOldPara(oldContent, pagePrototypeTypeStart, 15, "prototype-type", itemName).trim();
	var pageInternalNameStart = oldContent.search(/(\s|\|)internal-name/) + 14;
	var pageInternalName = getOldPara(oldContent, pageInternalNameStart, 14, "internal-name", itemName).trim();

	summary = "";
	newContent = "";
	if ((pageInternalName == internalName) && (pagePrototypeType == prototypeType)) {
		console.log(itemName + " page was not changed.")
	} else {
		if (pageInternalName != internalName) {
			newContent = oldContent;
			var newInternalNameStart = newContent.search(/(\s|\|)internal-name/) + 14;
			updatePara(newContent, internalName, pageInternalName, "internal-name", newInternalNameStart, 14, itemName);
		}
		if (pagePrototypeType != prototypeType) {
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPrototypeTypeStart = newContent.search(/(\s|\|)prototype-type/) + 15;
			updatePara(newContent, prototypeType, pagePrototypeType, "prototype-type", newPrototypeTypeStart, 15, itemName);
		}
	}
	if (newContent.length > 0) editPage("Infobox:" + itemName, itemName);
}

$("#EntityHealthUpdate").click(function(){
    getEntityHealth();
});

function getEntityHealth() {
	getUserGroup();
	if (userGroup.some(isBot) == false) return;
	var entityInput = prompt("Please enter the entity healths.");
	if (entityInput != null) {
		getToken();
		var entities = entityInput.split(/\s\s/g);
		console.log(entities.length + " entities detected");
		entities.forEach(updateEntityHealthInInfobox);
	}
}

function updateEntityHealthInInfobox(entity) {
	var entityNameEnd = entity.search("\\|");
	var entityName = entity.slice(0, entityNameEnd).trim();
	
	var entityHealth = getInputPara(entity, "\\|health = ", 10, "health", entityName).trim();
	
	//get page content of the tech -> oldContent
	var oldContent = "";
	$.ajax({
		url: apiUrl,
		data: {
			format: 'json',
			action: 'query',
			titles: 'Infobox:' + entityName,
			prop: 'revisions',
			rvprop: 'content'
		},
		async: false,
		dataType: 'json',
		type: 'GET',
		success: function( data ) {
			var pages = data.query.pages;
			var revisions = pages[Object.keys(pages)[0]].revisions[0];
			oldContent = revisions[Object.keys(revisions)[2]];
		},
		error: function( xhr ) {
			alert( 'Error: Request failed.' );
			oldContent = "";
		}
	});
	if (oldContent.length = 0) {
		console.log("No " + entityName + " page found.");
		return;
	}
	
	var pageEntityHealthStart = oldContent.search(/(\s|\|)health/) + 7;
	var pageEntityHealth = getOldPara(oldContent, pageEntityHealthStart, 7, "health", entityName).trim();
	
	summary = "";
	newContent = "";
	if (pageEntityHealth == entityHealth) {
		console.log(entityName + " page was not changed.")
	} else {
		newContent = oldContent;
		var newEntityHealthStart = newContent.search(/(\s|\|)health/) + 7;
		updatePara(newContent, entityHealth, pageEntityHealth, "health", newEntityHealthStart, 7, entityName);
		editPage("Infobox:" + entityName, entityName);
	}
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

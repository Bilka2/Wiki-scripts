/* Infobox updating */

var noInfobox = ["Basic oil processing", "Advanced oil processing", "Coal liquefaction", "Empty barrel", "Heavy oil cracking", "Light oil cracking", "Solid fuel from heavy oil", "Solid fuel from light oil", "Solid fuel from petroleum gas", "Water barrel", "Crude oil barrel", "Heavy oil barrel", "Sulfuric acid barrel", "Light oil barrel", "Petroleum gas barrel", "Lubricant barrel", "Empty crude oil barrel", "Empty heavy oil barrel", "Empty light oil barrel", "Empty lubricant barrel", "Empty petroleum gas barrel", "Empty sulfuric acid barrel", "Empty water barrel", "Fill crude oil barrel", "Fill heavy oil barrel", "Fill light oil barrel", "Fill lubricant barrel", "Fill petroleum gas barrel", "Fill sulfuric acid barrel", "Fill water barrel"]
var version = "0.15.12";


var para = "";
function getInputPara(item, search, length, name, itemName) {
	var paraStart = item.search(search) + length; //finds the beginning of the para, is after para-name
	if (paraStart < length) {
		console.log(itemName + ": No " + name + " found.");
		para = "";
	} else {
		var paraCut = item.slice(paraStart);  //lets the string begin after the parameter name
		var paraEnd = paraCut.search(/\||}}/); //finds the end of the parameter definition
		if (paraEnd < 1) { //para ends at para-end if it exists
			para = paraCut;
		} else {
			para = paraCut.slice(0, paraEnd);
		}
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
		if (pageParaEnd < 1) { //para ends at para-end if it exists
			pagePara = pageParaCut;
		} else {
			pagePara = pageParaCut.slice(0, pageParaEnd);
		}
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
		url: 'https://wiki.factorio.com/api.php',
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
	if (userGroup.some(isBot) == true) {
		var recipeInput = prompt("Please enter the recipes");
		if (recipeInput != null) {
			getToken();
			var items = recipeInput.split(/\s\s/g);
			console.log(items.length + " items detected");
			items.forEach(removeDuplicateRecipesAndUpdateInfobox);
		}
	}
};


function removeDuplicateRecipesAndUpdateInfobox(recipes) {
	var itemNameEnd = recipes.search("\\|");
	var itemName = recipes.slice(0, itemNameEnd);
	itemName = itemName.trim();
	
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
	
	var recipe = getInputPara(recipes, "\\|recipe = ", 10, "recipe", itemName);
	var totalRaw = getInputPara(recipes, "\\|total-raw = ", 13, "total-raw", itemName);
	var expRecipe = getInputPara(recipes, "\\|expensive-recipe = ", 20, "expensive-recipe", itemName);
	var expTotalRaw = getInputPara(recipes, "\\|expensive-total-raw = ", 23, "expensive-total-raw", itemName);
	
	//remove whitespace
	recipe = recipe.trim();
	totalRaw = totalRaw.trim();
	expRecipe = expRecipe.trim();
	expTotalRaw = expTotalRaw.trim();	
	
	
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
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			titles: itemName + '/infobox',
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
			var title = pages[Object.keys(pages)[0]].title;
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
	var pageRecipeStart = oldContent.search(/(\s|\|)recipe/) + 7;
	var pageRecipe = getOldPara(oldContent, pageRecipeStart, 7, "recipe", itemName);

	var pageTotalRawStart = oldContent.search(/(\s|\|)total-raw/) + 10;
	var pageTotalRaw = getOldPara(oldContent, pageTotalRawStart, 10, "total-raw", itemName);
	
	var pageExpRecipeStart = oldContent.search(/(\s|\|)expensive-recipe/) + 17;
	var pageExpRecipe = getOldPara(oldContent, pageExpRecipeStart, 17, "expensive-recipe", itemName);

	var pageExpTotalRawStart = oldContent.search(/(\s|\|)expensive-total-raw/) + 20;
	var pageExpTotalRaw = getOldPara(oldContent, pageExpTotalRawStart, 20, "expensive-total-raw", itemName);

	
	//remove whitespace
	pageRecipe = pageRecipe.trim();
	pageTotalRaw = pageTotalRaw.trim();
	pageExpRecipe = pageExpRecipe.trim();
	pageExpTotalRaw = pageExpTotalRaw.trim();
	
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
			if (newContent.length == 0) {
				newContent = oldContent
			}
			var newPageTotalRawStart = newContent.search(/(\s|\|)total-raw/) + 10;
			updatePara(newContent, totalRaw, pageTotalRaw, "total-raw", newPageTotalRawStart, 10, itemName);
		}
		if (pageExpRecipe != expRecipe) {
			if (newContent.length == 0) {
				newContent = oldContent
			}
			var newPageExpRecipeStart = newContent.search(/(\s|\|)expensive-recipe/) + 17;
			updatePara(newContent, expRecipe, pageExpRecipe, "expensive-recipe", newPageExpRecipeStart, 17, itemName);
		}
		if (pageExpTotalRaw != expTotalRaw) {
			if (newContent.length == 0) {
				newContent = oldContent
			}
			var newPageExpTotalRawStart = newContent.search(/(\s|\|)expensive-total-raw/) + 20;
			updatePara(newContent, expTotalRaw, pageExpTotalRaw, "expensive-total-raw", newPageExpTotalRawStart, 20, itemName);
		}
	}
	//alright, newContent should be defined, change page:
	if (newContent.length > 0) {
		editPage(itemName + "/infobox", itemName);
	}	
}

$("#ItemUpdate").click(function(){
    getItems();
});

function getItems() {
	getUserGroup();
	if (userGroup.some(isBot) == false) {
		return;
	}
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
	var itemName = item.slice(0, itemNameEnd);
	itemName = itemName.trim();
	
	//Remove items that don't have Infoboxes on the wiki
	noInfobox.forEach(function(infoboxName) {
	if (itemName == infoboxName) {
		console.log("Removed " + itemName + " from output.");
		itemName = "";
	}
	})
	if (itemName.length == 0) {
		return;
	}
	var consumers = getInputPara(item, "\\|consumers = ", 13, "consumers", itemName);
	var stackSize = getInputPara(item, "\\|stack-size = ", 14, "stack-size", itemName);
	var reqTech = getInputPara(item, "\\|required-technologies = ", 25, "required-technologies", itemName);
	

	consumers = consumers.trim();
	stackSize = stackSize.trim();
	reqTech = reqTech.trim();
	
	
	//get page content of the item -> oldContent
	var oldContent = "";
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			titles: itemName + '/infobox',
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
			var title = pages[Object.keys(pages)[0]].title;
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
	var pageConsumers = getOldPara(oldContent, pageConsumersStart, 10, "consumers", itemName);
	
	var pageStackSizeStart = oldContent.search(/(\s|\|)stack-size/) + 11;
	var pageStackSize = getOldPara(oldContent, pageStackSizeStart, 11, "stack-size", itemName);
	
	var pageReqTechStart = oldContent.search(/(\s|\|)required-technologies/) + 22;
	var pageReqTech = getOldPara(oldContent, pageReqTechStart, 22, "required-technologies", itemName);
	
	
	pageConsumers = pageConsumers.trim();
	pageStackSize = pageStackSize.trim();
	pageReqTech = pageReqTech.trim();	
	
	
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
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPageStackSizeStart = newContent.search(/(\s|\|)stack-size/) + 11;
			updatePara(newContent, stackSize, pageStackSize, "stack-size", newPageStackSizeStart, 11, itemName);
		}
		if (pageReqTech != reqTech) {
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPageReqTechStart = newContent.search(/(\s|\|)required-technologies/) + 22;
			updatePara(newContent, reqTech, pageReqTech, "required-technologies", newPageReqTechStart, 22, itemName);
		}
	}
	
	//alright, newContent should be defined, change page:
	if (newContent.length > 0) {
		editPage(itemName + "/infobox", itemName);
	}
}

$("#TechUpdate").click(function(){
    getTechnologies();
});

function getTechnologies() {
	getUserGroup();
		if (userGroup.some(isBot) == false) {
		return;
	}
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
	var techName = tech.slice(0, techNameEnd);
	techName = techName.trim();
	
	
	var cost = getInputPara(tech, "\\|cost = ", 8, "cost", techName);
	var costMulti = getInputPara(tech, "\\|cost-multiplier = ", 19, "cost-multiplier", techName);
	var expCostMulti = getInputPara(tech, "\\|expensive-cost-multiplier = ", 29, "expensive-cost-multiplier", techName);
	var reqTech = getInputPara(tech, "\\|required-technologies = ", 25, "required-technologies", techName);
	var allows = getInputPara(tech, "\\|allows = ", 10, "allows", techName);
	var effects = getInputPara(tech, "\\|effects = ", 11, "effects", techName);

	
	cost = cost.trim();
	costMulti = costMulti.trim();
	expCostMulti = expCostMulti.trim();
	reqTech = reqTech.trim();
	allows = allows.trim();
	effects = effects.trim();
	
	
	//get page content of the tech -> oldContent
	var oldContent = "";
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			titles: techName + ' (research)/infobox',
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
			var title = pages[Object.keys(pages)[0]].title;
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
	var pageCost = getOldPara(oldContent, pageCostStart, 6, "cost", techName);
	
	var pageCostMultiStart = oldContent.search(/(\s|\|)cost-multiplier/) + 16;
	var pageCostMulti = getOldPara(oldContent, pageCostMultiStart, 16, "cost-multiplier", techName);
	
	var pageExpCostMultiStart = oldContent.search(/(\s|\|)expensive-cost-multiplier/) + 26;
	var pageExpCostMulti = getOldPara(oldContent, pageExpCostMultiStart, 26, "expensive-cost-multiplier", techName);
	
	var pageReqTechStart = oldContent.search(/(\s|\|)required-technologies/) + 22;
	var pageReqTech = getOldPara(oldContent, pageReqTechStart, 22, "required-technologies", techName);
	
	var pageAllowsStart = oldContent.search(/(\s|\|)allows/) + 7;
	var pageAllows = getOldPara(oldContent, pageAllowsStart, 7, "allows", techName);
	
	var pageEffectsStart = oldContent.search(/(\s|\|)effects/) + 8;
	var pageEffects = getOldPara(oldContent, pageEffectsStart, 8, "effects", techName);

	
	pageCost = pageCost.trim();
	pageCostMulti = pageCostMulti.trim();
	pageExpCostMulti = pageExpCostMulti.trim();
	pageReqTech = pageReqTech.trim();
	pageAllows = pageAllows.trim();
	pageEffects = pageEffects.trim();
	
	
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
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPageCostMultiStart = newContent.search(/(\s|\|)cost-multiplier/) + 16;
			updatePara(newContent, costMulti, pageCostMulti, "cost-multiplier", newPageCostMultiStart, 16, techName);
		}
		if (pageExpCostMulti != expCostMulti) {
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPageExpCostMultiStart = newContent.search(/(\s|\|)expensive-cost-multiplier/) + 26;
			updatePara(newContent, expCostMulti, pageExpCostMulti, "expensive-cost-multiplier", newPageExpCostMultiStart, 26, techName);
		}
		if (pageReqTech != reqTech) {
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPageReqTechStart = newContent.search(/(\s|\|)required-technologies/) + 22;
			updatePara(newContent, reqTech, pageReqTech, "required-technologies", newPageReqTechStart, 22, techName);
		}
		if (pageAllows != allows) {
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPageAllowsStart = newContent.search(/(\s|\|)allows/) + 7;
			updatePara(newContent, allows, pageAllows, "allows", newPageAllowsStart, 7, techName);
		}
		if (pageEffects != effects) {
			if (newContent.length == 0) {
				newContent = oldContent;
			}
			var newPageEffectsStart = newContent.search(/(\s|\|)effects/) + 8;
			updatePara(newContent, effects, pageEffects, "effects", newPageEffectsStart, 8, techName);
		}	
	}
	//alright, newContent should be defined, change page:
	if (newContent.length > 0) {
		editPage(techName + " (research)/infobox", techName);
	}	
}

$("#AllUpdate").click(function(){
    getAll();
});

function getAll() {
	getUserGroup();
		if (userGroup.some(isBot) == false) {
		return;
	}
	getToken();
	newVersion = prompt("Please enter the new version.");
	if (newVersion != null) {
		version = newVersion.trim();
	}
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
		if (userGroup.some(isBot) == false) {
		return;
	}
	var techInput = prompt("Please enter the technology internal-names");
	if (techInput != null) {
		getToken();
		var techs = techInput.split(/\s\s/g);
		console.log(techs.length + " techs detected");
		techs.forEach(updateTechnologyDataInfobox);
	}
}

function updateTechnologyDataInfobox(tech) {
	var techNameEnd = tech.search("\\|");
	var techName = tech.slice(0, techNameEnd);
	techName = techName.trim();
	
	var internalName = getInputPara(tech, "\\|internal-name = ", 17, "internal-name", techName);
	internalName = internalName.trim();
	var prototypeType = "technology";
	
	//get page content of the tech -> oldContent
	var oldContent = "";
	$.ajax({
		url: 'https://wiki.factorio.com/api.php',
		data: {
			format: 'json',
			action: 'query',
			titles: techName + ' (research)/infobox',
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
			var title = pages[Object.keys(pages)[0]].title;
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
	var pageInternalName = getOldPara(oldContent, pageInternalNameStart, 14, "internal-name", techName);
	
	var pagePrototypeTypeStart = oldContent.search(/(\s|\|)prototype-type/) + 15;
	var pagePrototypeType = getOldPara(oldContent, pagePrototypeTypeStart, 15, "prototype-type", techName);
	
	pageInternalName = pageInternalName.trim();
	pagePrototypeType = pagePrototypeType.trim();
	
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
		editPage(techName + " (research)/infobox", techName);
	}
}
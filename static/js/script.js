const searchBox = document.querySelector(".search_field");
const inputBox = searchBox.querySelector("input");
const suggestionsBox = searchBox.querySelector(".autocom_box");

searchBox.onkeyup =(e)=>{
	let userInput = e.target.value;
	let emptyArray = [];
	if(userInput){
		emptyArray = getSuggestions(userInput).filter((data)=>{
			return data.toLowerCase().startsWith(userInput.toLocaleLowerCase());
		});
		emptyArray = emptyArray.map((data)=>{
			return data = '<li>'+ data + '</li>';
		});
		searchBox.classList.add("active");
		showSuggestions(emptyArray);
		let allList = suggestionsBox.querySelectorAll("li");
		for (let i = 0; i < allList.length; i++) {
			allList[i].setAttribute("onclick", "select(this)");
		}
	}else{
		searchBox.classList.remove("active");
	}
	
}

function select(element){
	let selectUserInput = element.textContent;
	inputBox.value = selectUserInput;
	console.log(inputBox.value);
	searchBox.classList.remove("active");
}

function showSuggestions(list){
	let listData;
	if (!list.length) {
		userInput = inputBox.value;
		listData = '<li>'+ userInput + '</li>';
	}else{
		listData = list.join('');
	}
	suggestionsBox.innerHTML = listData;
}

function getSuggestions(userInput){
	var jsonData = [];
	var jsonNamesData = [];
	$.ajax({
	  url: 'https://api.themoviedb.org/3/search/tv?api_key=a2b67da805cffb9ba951a0f56da1e603&query='+userInput,
	  async: false,
	  dataType: 'json',
	  success: function (json) {
	    jsonData = json;
	  }
	});
	for (var i = 0; i < 5; i++) {
		jsonNamesData.push(jsonData.results[i].name);
	}
	return jsonNamesData;
}
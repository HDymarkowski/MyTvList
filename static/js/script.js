const searchBox = document.querySelector(".search_field");
const inputBox = searchBox.querySelector("input");
const suggestionsBox = searchBox.querySelector(".autocom_box");

searchBox.onkeyup =(e)=>{
	let userInput = e.target.value;
	let emptyArray = [];
	if(userInput){
		emptyArray = getSuggestions(userInput);
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
	console.log(selectUserInput);
	inputBox.value = selectUserInput;
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
	if (!jsonData) {
		return jsonNamesData;
	}
	for (var i = 0; i < 5 && i < jsonData.results.length; i++) {
		jsonNamesData.push(jsonData.results[i].name);
	}
	return jsonNamesData;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
	$('.clickable').click(function(){
		$.post( "/MyTvList/showPage/", 
         { csrfmiddlewaretoken: getCookie('csrftoken'), name: $(this).attr('name')
         }, 
         function(data) {
             window.open("/MyTvList/showPage/");
        });
	});
});
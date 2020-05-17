function createCORSRequest(method, url) {
	var xhr = new XMLHttpRequest();
	if ("withCredentials" in xhr) {
		// Check if the XMLHttpRequest object has a "withCredentials" property.
		// "withCredentials" only exists on XMLHTTPRequest2 objects.
		xhr.open(method, url, true);
	} else if (typeof XDomainRequest != "undefined") {
		// Otherwise, check if XDomainRequest.
		// XDomainRequest only exists in IE, and is IE's way of making CORS requests.
		xhr = new XDomainRequest();
		xhr.open(method, url);
	} else {
		xhr = null;
	}
	return xhr;
};


function reset(all=false) {
	console.log("clear triggered");
	if (all === true)
		document.getElementById("textbox-result").value = "";
};


async function load() {
	var xhr = createCORSRequest("POST", "http://localhost:8080/activate");
	var configs = {"model_name": ""};
	if (document.getElementById("data_source").value === "women"){
		configs["model_name"] = "model_cwomen"
	} else if (document.getElementById("data_source").value === "men"){
		configs["model_name"] = "model_cmen"
	} else if (document.getElementById("data_source").value === "minyao"){
		configs["model_name"] = null
	};
	console.log(configs);
	var data = JSON.stringify({
		"configs": configs
			
	});
	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			console.log("model activation SUCCESS");
		}
	});
	xhr.setRequestHeader("Content-Type", "text/json");
	xhr.setRequestHeader("cache-control", "no-cache");

	xhr.send(data);

};


function compose() {
	var configs = {}
	if (document.getElementById("num_of_sentence").value){
		configs["num_of_sentence"] = parseInt(document.getElementById("num_of_sentence").value);
	} else {
		configs["num_of_sentence"] = 4;
	}
	if (document.getElementById("limit_word_size").value){
		configs["limit_word_size"] = parseInt(document.getElementById("limit_word_size").value);
	} else {
		configs["limit_word_size"] = 4;
	}

	console.log(configs);
	
	var data = JSON.stringify({
		"configs": configs
	});

	
	var xhr = createCORSRequest("POST", "http://localhost:8080/compose");
	
	if (!xhr) {
			alert('CORS not supported');
			return;
	};
	
	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === 4) {
			console.log(this.responseText);
			result = JSON.parse(this.responseText);
			var result_box = document.getElementById("textbox-result");
			var lyrics = result["response"];
			if (lyrics){
				result_box.value = lyrics
			} else { 
				result_box.value = "no return model error"
			}
		}
	});
	xhr.setRequestHeader("Content-Type", "text/json");
	xhr.setRequestHeader("cache-control", "no-cache");

	xhr.send(data);
}
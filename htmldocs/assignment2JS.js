function initialize(){

	$.ajax({
		//url: 'http://wt.ops.few.vu.nl/api/663753db',
		url: 'http://localhost:8080/database',
		success: function(data){
			$('#TableExerciseTable').dynatable({
				table: {
					bodyRowSelector: 'tbody.data tr'
				},	
				dataset: {
					records: data,
				}
			});
		}
	});

	
	$('#browserCompatibilityTable').dynatable();
	$('#internetProtocolTable').dynatable();
	$('#comparisonTable').dynatable();
	$('#ColorContrastTable').dynatable();
	

}

	function initMap() {
	var map;
	map = new google.maps.Map(document.getElementById('map'), {
	  center: {lat: -34.397, lng: 150.644},
	  zoom: 8
	});
	}



//Reload database data and update the page.
function updateData(){	
	//This function makes use of the dynatable library
	
	var dynatable = $('#TableExerciseTable').data('dynatable');	

	//Get data from server with HTTP:GET method.
	$.ajax({ 
	//url: 'http://wt.ops.few.vu.nl/api/663753db',
	url: 'http://localhost:8080/database',
	success: function(data){
		dynatable.settings.dataset.originalRecords = data;
		dynatable.process();
				}
	});						
}

function resetDatabase(){
	//This function makes use of the dynatable library

	$.get("http://wt.ops.few.vu.nl/api/663753db/reset");
	updateData();
}

function postForm(){
	
	var $form = $("form.formInput");
	
	if ($form[0].checkValidity()) {//check if form is valid
	
	//$.post("http://wt.ops.few.vu.nl/api/663753db", $form.serialize());//Send form data to the server in JSON format.
	$.post("http://localhost:8080/database", $form.serialize());//Send form data to the server in JSON format.
	
	updateData();//Update the table								
	}
}
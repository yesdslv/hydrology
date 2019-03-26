var hydropost;
//pass in POST request
var currentDate;
var year;
var month;
var day;
var months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", 
    "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"];
var hour;
var minute;
var time;
//To display string representation of date in modal(Год: year, Месяц: month, День: day)
var currentDateString;
//To display string represantation of time in modal(Час: hour, Минута: minute)
var currentTimeString;

$('select[name="hydropost"]').change(function() {
	hydropost = $(this).find("option:selected").text();
	$("#hydropost").text(hydropost);
	request = $.ajax({
		url: url_category,
		type: "GET",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		data: {
			"hydropost" : hydropost
		}
	});
	request.done(function(data) {
		category = data.category;
		$("#category").text(category);
	});
	request.fail(function(data) {
		console.log("error");
	});
});

//Set russian locale
$.datepicker.setDefaults($.datepicker.regional["ru"]);
$("#datepicker").datepicker({
	dateFormat: "yy-mm-dd",
	maxDate: 0,
	onSelect: function(date) {
		currentDate = date;
		//To transform to text
		var dateObject = new Date(date);
		year = dateObject.getFullYear();
		month = months[dateObject.getMonth()];
		day = dateObject.getDate();
		console.log(day);
		currentDateString = year + " год " + day + " " + month;
	}
});
$("#datepicker").datepicker("setDate", new Date());//Set today date

$('input[name="hour"]').change(function() {
      	var min = 0;
	var max = 23;
	hour = parseInt($('input[name="hour"]').val());
	if (hour < min) {
		$('input[name="hour"]').val(min);
		hour = min;	
	} else if (hour > max)  {
		$('input[name="hour"]').val(max);
		hour = max;
	}
	currentTimeString = "Час:" + hour + " минута:" + minute;
});

$('input[name="minute"]').change(function() {
      	var min = 0;
	var max = 59;
	minute = parseInt($('input[name="minute"]').val());
	if (minute < min) {
		$('input[name="minute"]').val(min);
		minute = min;
	} else if (minute > max)  {
		$('input[name="minute"]').val(max);
		minute = max;
	}
	currentTimeString = "Час:" + hour + " минута:" + minute;
});

$("#modalTrigger").click(function() {
	currentDatetime = currentDate + " " + hour + ":" + minute;
	$('#observationDate').text(currentDateString);
	$('#observationTime').text(currentTimeString);
	console.log(currentTimeString);
	$(".modal-body").load(url_record + "?" + $.param({ "category" : category }), 
		function(response, status, xhr) {
			//Initialize the selectpickers after loading the data
			$('.selectpicker').selectpicker();		
			if (status == "error") {
				var msg = "Sorry but there was an error: ";
				console.log(msg + xhr.status + " " + xhr.statusText);
				$(".modal-body").text("Ошибка 500");
			}
	});
});

$('button[name="save"]').click(function() {
	var csrftoken = $("[name=csrfmiddlewaretoken]").val();
	var observation = $('form').serializeArray();
	var offset = new Date().getTimezoneOffset();
	observation.push({ name: "category", value: category });
	observation.push({ name: "hydropost", value: hydropost });
	observation.push({ name: "date", value: currentDate });
	observation.push({ name: "hour", value: hour });
	observation.push({ name: "minute", value: minute });
	observation.push({ name: "offset", value: offset });
	request = $.ajax({
		type: "POST",
		url: url_record,
		beforeSend: function(xhr, settings) {
			$("#loading").show();
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
		data: $.param(observation)
	});
	request.done(function(data) {
		$("#loading").hide();
		$('button[name="save"]').hide();
		$("#fail").hide();
		$("#success").show();
		setTimeout(function() {
			$("#observationModal").modal("hide");
		}, 3000);
		console.log(data);
	});
	request.fail(function(data) {
		$("#loading").hide();
		$("#fail").hide();
		$("#fail > .alert").text(data.responseJSON.error);
		$("#fail").show();
	});
});	

//first page load
$('select[name="hydropost"]').trigger("change");
$('.ui-datepicker-today').trigger('click');
$('input[name="hour"]').trigger("change");
$('input[name="minute"]').trigger("change");

//On modal hide, return modal initial condition(show Save button, hide messages and loading gif)
$('#observationModal').on('hidden.bs.modal', function () {
	$("#success #fail #loading").hide();
	$('.container-fluid').hide();
	$('button[name="save"]').show();
});

$("select").on("changed.bs.select", function() {
	console.log("YOHOHO");
}); 

function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

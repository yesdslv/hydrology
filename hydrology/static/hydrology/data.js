//Use in max date for enddatetimepicker, User cannot choose date, that exceeds current datetime
var currentDate = moment().format('YYYY-MM-DD, HH:mm').toString() ;
var minDate = moment().subtract(7, 'days').format('YYYY-MM-DD, HH:mm').toString() ;
//Init start datepicker
$("#startdatetimepicker").datetimepicker({
	defaultDate: minDate,
        format: 'YYYY-MM-DD HH:mm:ss',
        locale: 'ru',
});
$("#enddatetimepicker").datetimepicker({
        defaultDate: currentDate,
        format: 'YYYY-MM-DD HH:mm:ss',
        locale: 'ru',
});

$("#startdatetimepicker").on("change.datetimepicker", function (e) {
        $('#enddatetimepicker').datetimepicker('minDate', e.date);
});
$("#enddatetimepicker").on("change.datetimepicker", function (e) {
        $('#startdatetimepicker').datetimepicker('maxDate', e.date);
});

	
$("#datatable").DataTable({
	"language": {
		"processing": "Подождите...",
  		"search": "Поиск по гидропостам:",
  		"lengthMenu": "Показать _MENU_ записей",
  		"info": "Записи с _START_ до _END_ из _TOTAL_ записей",
  		"infoEmpty": "Записи с 0 до 0 из 0 записей",
  		"infoFiltered": "(отфильтровано из _MAX_ записей)",
  		"infoPostFix": "",
  		"loadingRecords": "Загрузка записей...",
  		"zeroRecords": "Записи отсутствуют.",
  		"emptyTable": "В таблице отсутствуют данные",
  		"paginate": {
    			"first": "Первая",
    			"previous": "Предыдущая",
    			"next": "Следующая",
    			"last": "Последняя"
  		},
  		"aria": {
    			"sortAscending": ": активировать для сортировки столбца по возрастанию",
    			"sortDescending": ": активировать для сортировки столбца по убыванию"
  		}	
	},
	"serverSide": true,
	"processing": true,
	"ajax": {
		type: "POST",
		url: url_data,
		beforeSend: function(xhr, settings) {
			var csrftoken = Cookies.get('csrftoken');
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
		data: function(d) {
			var form_data = $("#startenddatetime").serializeArray();
			$.each(form_data, function(key, val) {
				d[val.name] = val.value;
			});
		}
	},
	dom: 'Bfrtip',
	buttons: [
		{
			extend: 'columnsToggle',
		        columns: [3, 4, 5, 6, 7, 8, 9, 10] 
		}	
		],
	"columnDefs": [
		{
			"searchable": false,
			"targets": [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		},
		{ "name": "details",   "targets": 0 },
		{ "name": "hydropost_name",  "targets": 1 },
		{ "name": "observation_datetime", "targets": 2 },
		{ "name": "level",  "targets": 3 },
		{ "name": "water_object_condition",    "targets": 4 },
		{ "name": "water_temperature",    "targets": 5 },
		{ "name": "air_temperature",    "targets": 6 },
		{ "name": "precipitation",    "targets": 7 },
		{ "name": "precipitation_type",    "targets": 8 },
		{ "name": "wind_direction",    "targets": 9 },
		{ "name": "wind_power",    "targets": 10 }
	],
	"columns" : [
		{
			"className": 'details-control',
			"orderable":      false,
			"data":           null,
			"defaultContent": ''
		},
		{"data": "hydropost_name"},
		{"data": "observation_datetime"},
		{"data": "level"},
		{"data": "water_object_condition"},
		{"data": "air_temperature"},
		{"data": "water_temperature"},
		{"data": "precipitation"},
		{"data": "precipitation_type"},
		{"data": "wind_power"},
		{"data": "wind_direction"},
	]
});

// Add event listener for opening and closing details
$('#datatable tbody').on('click', 'td.details-control', function () {
	var tr = $(this).closest('tr');
        var row = $("#datatable").DataTable().row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
});


function format ( d ) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Регион:</td>'+
            '<td>'+d.region+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Наблюдатель:</td>'+
            '<td>'+d.observer+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Время ввода информации:</td>'+
            '<td>'+d.entry_datetime+'</td>'+
        '</tr>'+
    '</table>';
}


$('a.toggle-vis').on( 'click', function (e) {
	e.preventDefault();
	// Get the column API object
	var column = table.column( $(this).attr('data-column') );
	// Toggle the visibility
	column.visible( ! column.visible() );
});

function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(".input-group").on("change.datetimepicker", function (e) {
	$("#datatable").DataTable().ajax.reload();
	e.preventDefault();
});

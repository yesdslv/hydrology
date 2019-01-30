var category;

$('[name="hydropost"]').change(function () {
     hydropost = $(this).val();
     
     $( "h2" ).replaceWith( "<h2>"+  hydropost +"</h2>" );
      $.ajax({
	      url: url_category,
	type: 'GET',
	contentType: "application/json; charset=utf-8",
	dataType: "json",
        data: {
          'hydropost': hydropost
        },
        success: function(data){ 
		category = data.category;
		$( "h3" ).replaceWith( "<h3>" + data.category + "</h3>" );
  	},
  	error: function(data){
    		$( "h3" ).replaceWith( "<h3>" + data.hydropost + "</h3>" );
  	}
      });
});

$('[name="hydropost"]').trigger("change") //first page load

$('.btn').click(function() {
	hydropost = $('select option:selected').val();
	console.log(hydropost);
	console.log(url_ogp2record);
	console.log(category);
	//console.log(typeof(url_category));
	//console.log(typeof(url_ogp2record));
	//$(".modal-body").on('load', url_ogp2record, { 'hydropost' : hydropost }, function() {
	//	  console.log( "The last 25 entries in the feed have been loaded" );
	//});
	//$(".modal-body").load(url_ogp2record,function(response, status, xhr) {
	//	if (status == "error") {
	//	    var msg = "Sorry but there was an error: ";
	//	    console.log(msg + xhr.status + " " + xhr.statusText);
	//	}
	//});
	$(".modal-body").load(String(url_ogp2record));
});

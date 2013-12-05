$(document).ready(function() {


	/*
	 * add highlight when feifei price is higher then others
	 */
	(function(){

		var itemNodes = $('#price_list tbody tr');

		for(var i=0; i < itemNodes.length; i++) {

			var fp = parseFloat( itemNodes[i].children[3].innerText );
			var tp = parseFloat( itemNodes[i].children[4].innerText.split('\n')[0] );
			var jp = parseFloat( itemNodes[i].children[5].innerText.split('\n')[0] );

			if( fp > tp || fp > jp ) {
				$(itemNodes[i]).addClass('highlight');
			}

		}

	}())

	/* 
	 * monitor template submit
	 */
	$(document).on('click', '#monitor-template-submit', function() {

		$.ajaxFileUpload({
			url : '/scraper/monitor/',
			type: "post",
			secureuri:false,
			fileElementId:'monitor-template',
			dataType: 'json',
			data: {},
			success: function (data, status){
				console.dir(data);
			},
			error: function (data, status, e) {
				alert(e);
			}
		});

	});


	$(document).on('click', '#template-download-btn', function() {
		$('#template-download-form').submit();
	});
	
});
$(document).ready(function() {

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
				console.log(data);
			},
			error: function (data, status, e) {
				alert(e);
			}
		});

	});
	
});
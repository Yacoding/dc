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
			var yxp = parseFloat( itemNodes[i].children[6].innerText.split('\n')[0] );
			var yhdp = parseFloat( itemNodes[i].children[7].innerText.split('\n')[0] );
			var ap = parseFloat( itemNodes[i].children[8].innerText.split('\n')[0] );

			if( fp > tp || fp > jp || fp > yxp || fp > yhdp || fp > ap ) {
				$(itemNodes[i]).addClass('highlight');
			}

		}

	}())

	/* 
	 * monitor template submit
	 */
	$(document).on('click', '#monitor-template-submit', function() {

		$.ajaxFileUpload({
			url : '/monitor/template/',
			type: "post",
			secureuri:false,
			fileElementId:'monitor-template',
			dataType: 'json',
			data: {},
			success: function (data, status){
				if(data.status === 'success') {
					$('#uploadSuccessModal .modal-body').html('<p>上传任务成功</p><p>服务器将在30min内开始抓取任务</p>');
					$('#uploadSuccessModal').modal();
				}
				else {
					$('#uploadSuccessModal .modal-body').html('<p>上传任务错误</p>');
					$('#uploadSuccessModal').modal();
				}
			},
			error: function (data, status, e) { console.log(e); }
		});

	});


	$('#template-download-btn').click(function(){
		$('#template-download-form').submit();
	});

	
});
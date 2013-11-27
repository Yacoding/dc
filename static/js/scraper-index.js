$(document).ready(function() {

	/* 
	 * single-scraper
	 * Submit Tasks of Tmall 
	 */
	$(document).on('click', '#single-scraper-submit', function() {

		var sendData = { 'tasks': [] };
		task = {
			category : '',
			start_url : $('#single-scraper-start-url').val()
		};
		sendData.tasks.push( task );
		sendData.source = $('#single-scraper-source').val();
		sendData.type = 'BUSINESS_CALL';

		console.log( JSON.stringify(sendData) );

		var self = $(this);
		self.attr('disabled', true);
		self.html('正在抓取');

		$.ajax({
			url : '/scraper/crawl/',
			type: 'POST',
			data: JSON.stringify(sendData),
			success: function(data){
				rto = JSON.parse(data);
				file_name = rto.content;
				addExcelDownloadForm( file_name );

				self.html('抓取完成');

				alert( '让您久等，终于抓完了！' );
			},
			error: function(data){
				console.log(data);
			}
		});

		var addExcelDownloadForm = function(file_name) {
			var html = 	'<div class="panel panel-success">' +
						'<div class="panel-heading">Excel文件下载</div>' +
						'<div class="panel-body">' +
							'<div class="alert alert-success alert-dismissable">' +
								'<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
								'<strong>注意! </strong>' +
								'您提交的链接已抓取完成，点击“下载”按钮，下载Excel文件' +
							'</div>' +
							'<form id="download-excel-form" action="/scraper/download/" method="POST">' +
								'<input type="hidden" name="file_name" value="' + file_name + '" />' +
								'<button type="submit" id="download-excel" class="btn btn-success">下载 Download</button>' +
							'</form>' +
						'</div>' +
			        '</div>';
			$(html).insertAfter('#single-scraper-panel');
		};
	});

	

});
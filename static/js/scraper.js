$(document).ready(function() {

	/* Get The List of Tmall's Category */
	$(document).on('click', '#cat-btn', function(){

		var sendData = {};
		sendData.source = $('#cat-source').val();
		sendData.action = $('#cat-action').val();

		$.ajax({

			url:'/scraper/category/',
			get:'GET',
			data: sendData,

			success: function( data ){

				var data = JSON.parse( data );
				var cat = data['content']['cat'];
				var zNodes = [];


				for(var first in cat) {
					if( first in TMALL_CAT ) {
						zNodes.push({ id: first, pId: 0, name: first });
						for(var second in cat[first]) {
							zNodes.push({
								id: second, pId: first,
								name: second,
								url : cat[first][second],
								target : '_blank',
							});
						}
					}
				}

				var setting = {
					check: { enable: true, chkboxType: { Y : 'ps', N : 'ps' } },
					data: { simpleData: { enable: true } }
				};

				$.fn.zTree.init($("#show"), setting, zNodes);

			},
			error:function(data){
				console.log('error');
			}
		});
	});

	/* Tamll' Category that We Want */
	var TMALL_CAT = {
		'旅行箱包':     'lx',
		'男士护肤':     'hf',
		'个人洗护':     'xh',
		'厨房电器':     'cf',
		'生活电器':     'sh',
		'个人护理':     'hl',
		'精品家具':     'jj',
		'灯饰照明':     'zm',
		'厨卫装修':     'cw',
		'五金电工':     'wj',
		'精品家纺':     'jf',
		'冬季床品':     'cp',
		'布艺软饰':     'by',    
		'家居饰品':     'sp',
		'居家日用':     'ry',
		'厨房餐饮':     'cy',
		'计生用品':     'js'
	};

	/* Submit Tasks of Tmall */
	$(document).on('click', '#submit-tm-task-btn', function() {

		var nodes = $('li.level1');
		var tasks = [];
		var rto = {};

		nodes.each(function(){
			var flag = $(this).find('span.chk').hasClass('checkbox_true_full');
			if( flag ) {
				var task = {};
				task.category = [];
				task.category.push( $(this).parent().siblings('a').attr('title') );
				task.category.push( $(this).find('a').attr('title') );
				task.url = $(this).find('a').attr('href');
				task.source = 'tmall';
				tasks.push( task );
			}			
		});
		rto.tasks = tasks;

		$.ajax({
			url : '/scraper/crawl/',
			type: 'POST',
			data: rto,
			success: function(data){
				console.log('submit success', data);
			},
			error: function(data){
				console.log('submit error', data);
			}
		});
	});

});
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
				console.dir(data);
				_showPrice(data.content);
			},
			error: function (data, status, e) {
				alert(e);
			}
		});

	});

	var T_head = '<table cellpadding="0" cellspacing="0" border="0" class="" id="products">'+
						'<thead>'+
                            '<tr role="row">'+
                                '<th>缩略图</th>'+
								'<th>飞飞商品名</th>'+
								'<th>飞飞价</th>'+
								'<th>天猫商品名</th>'+
								'<th>天猫价</th>'+
								'<th>京东商品名</th>'+
								'<th>京东价</th>'+
                            '</tr>'+
                        '</thead>'+
                        '<tbody>';

    var T_foot = '</tbody></table>';

	var _showPrice = function( data ) {
		// 移除datatable对象绑定
		// ptable.fnDestroy();
		// // 清除product table
		// var parent_node = $('#product-parent');		
		// parent_node.empty();

		// var priceList = ''
		// data.sort(function(a,b){
		// 	if( a.gid == b.gid )
		// 		return a.main - b.main;				
		// 	else
		// 		return a.gid - b.gid;
		// });

		console.dir( data );

		// pack = [];


		// // 获取商品列表            
		// var productsList = '';
		// data = JSON.parse(data);
		// // update products
		// data.products.forEach(function(item){
		// 	productsList = productsList + '<tr><td><img src="' + item.img + '" width="60" /></td>'
		// 				 + '<td><a href="' + (item.url||'') + '" target="_blank">' + (item.name||PLACE_HOLDER) + '</a></td>' 
		// 				 + '<td>' + (item.category.join('/')||PLACE_HOLDER) + '</td>'
		// 				 + '<td>' + (item.price||PLACE_HOLDER) + '</td>'
		// 				 + '<td>' + (item.tm_moonSellCount||PLACE_HOLDER) + '</td>' 
		// 				 + '<td>' + (item.comment||PLACE_HOLDER) + '</td>'
		// 				 + '<td>' + (item.brand||PLACE_HOLDER) + '</td>' 
		// 				 + '<td>-</td>'
		// 				 + '<td class="center"><input type="checkbox" name="' + (item.sku||null) + '"></td></tr>';
		// });

		// parent_node.append( T_head + productsList + T_foot );

		// // 重新渲染datatable
		// window.ptable = $('#products').dataTable({
  //           "sPaginationType": "full_numbers",
  //           "aLengthMenu": [100, 50, 25],
  //           "iDisplayLength": 100
  //       });
	};
	
});
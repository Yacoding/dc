$(function(){

	(function(){

		var getFormJson = function(form) {
			var obj = {};
			var arr = $(form).serializeArray();
			$.each(arr, function(){
				if( obj[this.name] !== undefined ) {
					if ( ! obj[this.name].push ) {
		                obj[this.name] = [obj[this.name]];
		            }
					obj[this.name].push(this.value || '');
				} else {
					obj[this.name] = this.value || '';
				}
			});
			return obj;
		};

		/* 
		 * 选择来源、分类和排序
		 */
		$(document).on('click', '.dropdown-menu li a', function() {
			var info = $(this).html()
			  , data = $(this).attr('data')
			  , datafor = $(this).attr('for');
			// change the showing info
			$(this).parents('.btn-group').find('.display-info').html( info );
			// change the value of form's input
			$('#select-products input[name="' + datafor + '"]').attr({'value': data});

			if( datafor === 'source' ) {
				var sendData = {};
				sendData.source = data;

				$.ajax({
					url : '/radar/getCategory',
					type : 'POST',
					data : sendData,
					success : function(data) {
						data = JSON.parse(data);
						var cat = $('#category  ul');
						cat.empty();
						$('#category .display-info').html( '-' );
						$('#select-products input[name="category"]').attr({'value': ''});
						var str = '';
						for( var first in data ) {
							var tmp = first.replace(/\//g, '-');
							// console.log( first.constructor, first, data[first], data[first].constructor );
							str = str + '<li class="coll" data-submenu-id="' + tmp + '">';
							str = str + '<a for="category" data="' + first + '" class="">' + first + '</a>';
							str = str + '<div id="' + tmp + '" class="popover">';	
							str = str + '<p class="popover-title">' + first + '</p>';					
							if( data[first].constructor === Object ) {
								// for JD, level 3
								for( var second in data[first] ) {
									str = str + '<div class="popover-content">';
									str = str + '<ul class="second">';
									str = str + '<li>';
									str = str + '<p><a for="category" data="' + second + '">' + second + '</a></p>';
									str = str + '<ul class="third">';
									for( var third in data[first][second] ) {
										str = str + '<li><a for="category" data="' + data[first][second][third] + '">' + data[first][second][third] + '</a></li>';
									}
									str = str + '</ul>';
									str = str + '</li>';
									str = str + '</ul>';
									str = str + '</div>';
								}
							}
							else if( data[first].constructor === Array ) {
								// for Tmall, level 2
								str = str + '<div class="popover-content">';
								str = str + '<ul class="second">';
								str = str + '<li>';
								str = str + '<ul class="third">';
								data[first].forEach(function(second){
									if( second ) str = str + '<li><a for="category" data="' + second + '">' + second + '</a></li>';
								});
								str = str + '</ul>';
								str = str + '</li>';
								str = str + '</ul>';
								str = str + '</div>';
							}
							str = str + '</div>';
							str = str + '</li>';
						}						
						cat.append( str );

						dropdown();
					},
					error : function(XMLHttpRequest, textStatus, errorThrown) {
						console.log( 'get category ajax error' + errorThrown );
					}
				});
			}
			else if( datafor === 'category' ) {
				$('#select-products input[name="collection"]').attr({'value': $(this).parents('li.coll').attr('data-submenu-id')});
			}
		});

		/* 
		 * 点击页码，前一页，后一页
		 */
		$('.pager li a').click(function() {
			var data = $(this).attr('data');
			// change the value of form's input
			$('#select-products input[name="page"]').attr({'value': data});
			submitSelProForm($('#select-products'));
		});

		/* 
		 * 选择页码，跳到第几页
		 */
		$('.pager button').click(function() {
			var data = $('.pager input').val();
			// change the value of form's input
			$('#select-products input[name="page"]').attr({'value': data});
			submitSelProForm($('#select-products'));
		});

		/* 
		 * 提交商品显示表单
		 */
		$('#submit-sel-pro').click(function() {
			$('#select-products input[name="operation"]').attr({'value': 'SHOW_PRODUCTS'});
			submitSelProForm($('#select-products'));
		});

		/*
		 * 实际提交表单
		 */
		var submitSelProForm = function( form ) {
			form = form || $('#select-products');
			console.dir( getFormJson(form) );
			// ajax request
			$.ajax({
				url : '/radar/selectProducts',
				type : 'POST',
				data : getFormJson(form),
				success : function(data) {
					_showProducts(data);
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
					console.log( 'submitSelProForm ajax error' + errorThrown );
				}
			});
		}

		var PLACE_HOLDER = '-';

		var T_head = '<table cellpadding="0" cellspacing="0" border="0" class="" id="products">'+
						'<thead>'+
                            '<tr role="row">'+
                                '<th>缩略图</th>'+
								'<th width="200">商品名</th>'+
								'<th>分类</th>'+
								'<th>价格</th>'+
								'<th>销量</th>'+
								'<th>评论数</th>'+
								'<th>品牌</th>'+
								'<th>操作</th>'+
								'<th width="180"><button id="all-select" class="btn btn-info btn-xs">全选</button> <button id="compare" class="btn btn-primary btn-xs">对比</button> <button id="export" class="btn btn-success btn-xs">导出</button></th>'+
                            '</tr>'+
                        '</thead>'+
                        '<tbody>';

        var T_foot = '</tbody></table>';

		/* 
		 * 商品显示
		 */
		var _showProducts = function( data ) {
			// 移除datatable对象绑定
			ptable.fnDestroy();
			// 清除product table
			var parent_node = $('#product-parent');		
			parent_node.empty();
			// 获取商品列表            
			var productsList = '';
			data = JSON.parse(data);
			// update products
			data.products.forEach(function(item){
				productsList = productsList + '<tr><td><img src="' + item.img + '" width="60" /></td>'
							 + '<td><a href="' + (item.url||'') + '" target="_blank">' + (item.name||PLACE_HOLDER) + '</a></td>' 
							 + '<td>' + (item.category.join('/')||PLACE_HOLDER) + '</td>'
							 + '<td>' + (item.price||PLACE_HOLDER) + '</td>'
							 + '<td>' + (item.tm_moonSellCount||PLACE_HOLDER) + '</td>' 
							 + '<td>' + (item.comment||PLACE_HOLDER) + '</td>'
							 + '<td>' + (item.brand||PLACE_HOLDER) + '</td>' 
							 + '<td>-</td>'
							 + '<td class="center"><input type="checkbox" name="' + (item.sku||null) + '"></td></tr>';
			});

			parent_node.append( T_head + productsList + T_foot );
			// update pages
			_showPages(parseInt(data.page.current), parseInt(data.page.total));	

			// 重新渲染datatable
			window.ptable = $('#products').dataTable({
                "sPaginationType": "full_numbers",
                "aLengthMenu": [10, 25, 50],
                "iDisplayLength": 50,
                "oLanguage": {
                	"sSearch":"在结果中搜索：" ,
                	"sLengthMenu": "每页显示 _MENU_ 条记录",
                	"sInfo": "当前显示 _START_ 到 _END_ 条记录，共 _TOTAL_ 条记录",
                	"sZeroRecords": "对不起，查询不到相关数据！",
                	"oPaginate": {
                        "sFirst": "首页",
                        "sPrevious": "上一页",
                        "sNext": "下一页",
                        "sLast": "末页"
                    }
                } 
            });
		};

		/*
		 * 页码显示
		 */
		var _showPages = function( current, total ) {
			var pagerLi = $('.pager li a');
			$(pagerLi[1]).attr({'data': Math.max(1, current-1)});
			$(pagerLi[2]).attr({'data': current});
			$(pagerLi[2]).html( current );
			$(pagerLi[3]).attr({'data': Math.min(1+current, total)});
			$(pagerLi[4]).attr({'data': total});
			$('.pager span').html( total );
		};

		var initOperations = function() {

		}
		/*
		 * 全选事件
		 */
		$(document).on('click', '#all-select', function() {
			var checkbox = $('#products input[type="checkbox"]');
			var checked = $(checkbox).prop("checked");
			if( checked == true || checked === "checked" ) $(checkbox).prop("checked", false);
			else $(checkbox).prop("checked", true);
		});

		/*
		 * 商品对比
		 */
		$(document).on('click', '#compare', function() {
			if( ! $(form).find('input[name="items"]').attr('value') ) {
				alert( "请选择商品" );
				return;
			}

			var selectList = [];
			$('#products input[type="checkbox"]').each(function() {
				if( this.checked == true ) {
					selectList.push(this.name);
				}
			});

			var form = $('#select-products');
			$(form).find('input[name="operation"]').attr({'value' : 'DETAIL_PAGE'});
			$(form).find('input[name="items"]').attr({'value' : selectList.join(',')});

			$('#select-products').submit();		
		});

		/*
		 * 导出商品
		 */
		$(document).on('click', '#export', function() {
			if( ! $(form).find('input[name="items"]').attr('value') ) {
				alert( "请选择商品" );
				return;
			}

			var selectList = [];
			$('#products input[type="checkbox"]').each(function() {
				if( this.checked == true ) {
					selectList.push(this.name);
				}
			});

			var form = $('#select-products');
			$(form).find('input[name="operation"]').attr({'value' : 'EXPORT_PRODUCTS'});
			$(form).find('input[name="items"]').attr({'value' : selectList.join(',')});

			$('#select-products').submit();	
		});

		/*
		 * 导出全部商品
		 */
		$('#export-all').click(function(){
			if( ! $(form).find('input[name="category"]').attr('value') ) {
				alert( "请选择目录" );
				return;
			}

			var form = $('#select-products');
			$(form).find('input[name="operation"]').attr({'value' : 'EXPORT_PRODUCTS'});
			$(form).find('input[name="export_all"]').attr({'value' : 'true'});

			$('#select-products').submit();	
		});

	}());

});
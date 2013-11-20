$(function(){

	window.showProducts = function( products ){
		headerObj = _tableHeaderObj( products );
		header = _tableHeader( headerObj );
		body = _tableBody( products, headerObj );
		table = header + body;
		node = $('#products');
		node.empty();
		node.append( table );
		delete header;
		delete body;
		delete node;
		delete table;
		window.ptable = $('#products').dataTable({
            "sPaginationType": "full_numbers",
            "aLengthMenu": [10, 25, 50],
            "iDisplayLength": 50
        });
	};


	var _tableHeaderObj = function( products ) {	
        attr = {};
        products.forEach(function(pro){
        	for( var i in pro.attr ) {
        		if( ! attr[i] ) {
        			attr[i] = 1;
        		}
        	}
        });
        return attr;
	};

	var _tableHeader = function( obj ) {
		header = '<thead><tr role="row">' + 
					'<th>缩略图</th>' +
					'<th>商品名</th>' +
					'<th>分类</th>' +
					'<th>价格</th>' +
					'<th>销量</th>' +
					'<th>评论数</th>' +
					'<th>品牌</th>';
		for( var i in obj ) {
        	header += '<th>' + i + '</th>';
        }
        header += '</tr></thead>';		
		return header;
	};

	var _tableBody = function( products, header ) {
		body = '<tbody>';
		products.forEach(function(pro) {
			str = '<tr>' + 
					'<td><a href="' + pro["url"] + '" target="_blank"><img src="' + pro["img"] + '" /></a></td>' + 
					'<td>' + pro["name"] + '</td>' + 
					'<td>' + pro["category"] + '</td>' + 
					'<td>' + pro["price"] +  '</td>' +
					'<td>' + pro["tm_moonSellCount"] + '</td>' +
					'<td>' + pro["comment"] + '</td>' +
					'<td>' + pro["brand"] + '</td>';
			for( var i in header ) {
				if( i in pro.attr ) {
					str += '<td>' + pro.attr[i] + '</td>';
				}
				else {
					str += '<td></td>';
				}
			}
			str += '</tr>';
			body += str;
		});
		body += "</tbody>";
		return body;
	};

}());
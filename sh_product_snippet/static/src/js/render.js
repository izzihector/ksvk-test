odoo.define('sh_product_snippet.render', function (require) {
'use strict';

require('web.dom_ready');
var ajax = require('web.ajax');
var core = require('web.core');
var _t = core._t;


var qweb = core.qweb;


//A $( document ).ready() block.
$( document ).ready(function() {

	
//document ready start here	

	
	
	/*
	 * ***************************************
	 * sh_product_snippet_tmpl_1 JS
	 * **************************************
	 */
	function render_product_list($el) {
        
        
    	//alert("helo all");
        //this = element;
    	//var self = this;        	
    	var class_name = $el.attr('class');
	    	var category_id = false;
	    	var is_show_add_to_cart = false;
	    	var is_show_product_desc = false;
	    	var is_show_sale_price = false;
	    	var is_show_wish_list = false;
	    	var limit = false;
	    	var order_by = false;
	    	
	    	
	    	if(class_name){

	    		//for category 
	    		var js_category_id = class_name.match("sh_ecom_categ_(.*)_cend");
	
	    		
	    		if(js_category_id && js_category_id.length == 2){
	    			category_id = js_category_id[1];
	    		} 	    		

	    		//limit 
	    		var js_limit = class_name.match("sh_limit_(.*)_lend");
	    		if(js_limit && js_limit.length == 2){
	    			limit = js_limit[1];
	    		} 	    		
	    		
	    		//add to cart
	    		if($el.hasClass( "is_show_add_to_cart" )){
	    			is_show_add_to_cart = true;
	    		}
	    		
	    		//product description
	    		if($el.hasClass( "is_show_product_desc" )){
	    			is_show_product_desc = true;
	    		}

	    		//sale price
	    		if($el.hasClass( "is_show_sale_price" )){
	    			is_show_sale_price = true;
	    		} 	    		

	    		//wish list
	    		if($el.hasClass( "is_show_wish_list" )){
	    			is_show_wish_list = true;
	    		}  	    		
	    		
	    		/*
	    		 * ======================================= 
	    		*  order by
	    		* ========================================
	    		*/
	    		
	    		if($el.hasClass( "name_asc" )){
	    			order_by = 'name_asc';
	    		}  	   
	    		
	    		if($el.hasClass( "name_desc" )){
	    			order_by = 'name_desc';
	    		}  	   
	    		
	    		if($el.hasClass( "create_date_asc" )){
	    			order_by = 'create_date_asc';
	    		}  	   
	    		
	    		if($el.hasClass( "create_date_desc" )){
	    			order_by = 'create_date_desc';
	    		}  	   
	    		
	    		if($el.hasClass( "sale_price_asc" )){
	    			order_by = 'sale_price_asc';
	    		}  	   
	    		
	    		if($el.hasClass( "sale_price_desc" )){
	    			order_by = 'sale_price_desc';
	    		}  	   
	    		
	    		
	    	}

	    	ajax.jsonRpc('/sh_product_snippet/get_products', 'call', 
	       	 	{       
	    		'category_id' : category_id,
	    		'is_show_add_to_cart':is_show_add_to_cart,
	    		'is_show_product_desc':is_show_product_desc,
	    		'is_show_sale_price' : is_show_sale_price,
	    		'is_show_wish_list': is_show_wish_list,
	    		'limit' : limit,
	    		'order_by' : order_by,
	    		
	   		    }).then(function (data) {
	
	   		        $('#js_id_sh_product_snippet_div_row').replaceWith(data);
	   		        
	   		       $("#sh_product_snippet_loader").hide();

	            });    
	    	
        
        
        
        
    }
	
	
	
	
	
	
	
	
	
	
	
	var $snippet_sections = $("#sh_product_snippet_section_1");
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				//show loading bar
				 $("#sh_product_snippet_loader").show();
				 
				 render_product_list( $( this ) );
			
	
		});
			
		}
			

		
		
		
		
		
		
		
		/*
		 * ***************************************
		 * sh_product_snippet_tmpl_2 JS
		 * **************************************
		 */
		function render_product_list_2($el) {
	        
	        
	    	//alert("helo all");
	        //this = element;
	    	//var self = this;        	
	    	var class_name = $el.attr('class');
		    	var category_id = false;
		    	var is_show_add_to_cart = false;
		    	var is_show_product_desc = false;
		    	var is_show_sale_price = false;
		    	var is_show_wish_list = false;
		    	var limit = false;
		    	var order_by = false;
		    	
		    	
		    	if(class_name){

		    		//for category 
		    		var js_category_id = class_name.match("sh_ecom_categ_(.*)_cend");
		
		    		
		    		if(js_category_id && js_category_id.length == 2){
		    			category_id = js_category_id[1];
		    		} 	    		

		    		//limit 
		    		var js_limit = class_name.match("sh_limit_(.*)_lend");
		    		if(js_limit && js_limit.length == 2){
		    			limit = js_limit[1];
		    		} 	    		
		    		
		    		//add to cart
		    		if($el.hasClass( "is_show_add_to_cart" )){
		    			is_show_add_to_cart = true;
		    		}
		    		
		    		//product description
		    		if($el.hasClass( "is_show_product_desc" )){
		    			is_show_product_desc = true;
		    		}

		    		//sale price
		    		if($el.hasClass( "is_show_sale_price" )){
		    			is_show_sale_price = true;
		    		} 	    		

		    		//wish list
		    		if($el.hasClass( "is_show_wish_list" )){
		    			is_show_wish_list = true;
		    		}  	    		
		    		
		    		/*
		    		 * ======================================= 
		    		*  order by
		    		* ========================================
		    		*/
		    		
		    		if($el.hasClass( "name_asc" )){
		    			order_by = 'name_asc';
		    		}  	   
		    		
		    		if($el.hasClass( "name_desc" )){
		    			order_by = 'name_desc';
		    		}  	   
		    		
		    		if($el.hasClass( "create_date_asc" )){
		    			order_by = 'create_date_asc';
		    		}  	   
		    		
		    		if($el.hasClass( "create_date_desc" )){
		    			order_by = 'create_date_desc';
		    		}  	   
		    		
		    		if($el.hasClass( "sale_price_asc" )){
		    			order_by = 'sale_price_asc';
		    		}  	   
		    		
		    		if($el.hasClass( "sale_price_desc" )){
		    			order_by = 'sale_price_desc';
		    		}  	   
		    		
		    		
		    	}

		    	ajax.jsonRpc('/sh_product_snippet/get_snippet_2_products', 'call', 
		       	 	{       
		    		'category_id' : category_id,
		    		'is_show_add_to_cart':is_show_add_to_cart,
		    		'is_show_product_desc':is_show_product_desc,
		    		'is_show_sale_price' : is_show_sale_price,
		    		'is_show_wish_list': is_show_wish_list,
		    		'limit' : limit,
		    		'order_by' : order_by,
		    		
		   		    }).then(function (data) {
		
		   		        $('#js_id_sh_product_snippet_section_div_row_2').replaceWith(data);
		   		        
		   		       $("#sh_product_snippet_loader").hide();

		            });    
		    	
	        
	        
	        
	        
	    }
		
		
		
		
		
		
		
		
		
		
		
		var $snippet_sections = $("#sh_product_snippet_section_2");
			if($snippet_sections && $snippet_sections.length){
				
				$snippet_sections.each(function( index ) {
					
					//show loading bar
					 $("#sh_product_snippet_loader").show();
					 
					 render_product_list_2( $( this ) );
				
		
			});
				
			}
						
		
	
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			/*
			 * ***************************************
			 * sh_product_snippet_tmpl_2 JS
			 * **************************************
			 */
			function render_product_list_3($el) {
		        
		        
		    	//alert("helo all");
		        //this = element;
		    	//var self = this;        	
		    	var class_name = $el.attr('class');
			    	var category_id = false;
			    	var is_show_add_to_cart = false;
			    	var is_show_product_desc = false;
			    	var is_show_sale_price = false;
			    	var is_show_wish_list = false;
			    	var limit = false;
			    	var order_by = false;
			    	
			    	
			    	if(class_name){

			    		//for category 
			    		var js_category_id = class_name.match("sh_ecom_categ_(.*)_cend");
			
			    		
			    		if(js_category_id && js_category_id.length == 2){
			    			category_id = js_category_id[1];
			    		} 	    		

			    		//limit 
			    		var js_limit = class_name.match("sh_limit_(.*)_lend");
			    		if(js_limit && js_limit.length == 2){
			    			limit = js_limit[1];
			    		} 	    		
			    		
			    		//add to cart
			    		if($el.hasClass( "is_show_add_to_cart" )){
			    			is_show_add_to_cart = true;
			    		}
			    		
			    		//product description
			    		if($el.hasClass( "is_show_product_desc" )){
			    			is_show_product_desc = true;
			    		}

			    		//sale price
			    		if($el.hasClass( "is_show_sale_price" )){
			    			is_show_sale_price = true;
			    		} 	    		

			    		//wish list
			    		if($el.hasClass( "is_show_wish_list" )){
			    			is_show_wish_list = true;
			    		}  	    		
			    		
			    		/*
			    		 * ======================================= 
			    		*  order by
			    		* ========================================
			    		*/
			    		
			    		if($el.hasClass( "name_asc" )){
			    			order_by = 'name_asc';
			    		}  	   
			    		
			    		if($el.hasClass( "name_desc" )){
			    			order_by = 'name_desc';
			    		}  	   
			    		
			    		if($el.hasClass( "create_date_asc" )){
			    			order_by = 'create_date_asc';
			    		}  	   
			    		
			    		if($el.hasClass( "create_date_desc" )){
			    			order_by = 'create_date_desc';
			    		}  	   
			    		
			    		if($el.hasClass( "sale_price_asc" )){
			    			order_by = 'sale_price_asc';
			    		}  	   
			    		
			    		if($el.hasClass( "sale_price_desc" )){
			    			order_by = 'sale_price_desc';
			    		}  	   
			    		
			    		
			    	}

			    	ajax.jsonRpc('/sh_product_snippet/get_snippet_3_products', 'call', 
			       	 	{       
			    		'category_id' : category_id,
			    		'is_show_add_to_cart':is_show_add_to_cart,
			    		'is_show_product_desc':is_show_product_desc,
			    		'is_show_sale_price' : is_show_sale_price,
			    		'is_show_wish_list': is_show_wish_list,
			    		'limit' : limit,
			    		'order_by' : order_by,
			    		
			   		    }).then(function (data) {
			
			   		        $('#js_id_sh_product_snippet_section_div_row_3').replaceWith(data);
			   		        
			   		       $("#sh_product_snippet_loader").hide();

			            });    
			    	
		        
		        
		        
		        
		    }
			
			
			
			
			
			
			
			
			
			
			
			var $snippet_sections = $("#sh_product_snippet_section_3");
				if($snippet_sections && $snippet_sections.length){
					
					$snippet_sections.each(function( index ) {
						
						//show loading bar
						 $("#sh_product_snippet_loader").show();
						 
						 render_product_list_3( $( this ) );
					
			
				});
					
				}			
			
			
			
		
		
//document ready ends here.
		
});





});
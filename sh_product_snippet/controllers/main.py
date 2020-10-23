# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http, fields, _
from odoo.exceptions import UserError

class main(http.Controller):
    
    
    def _default_website(self):
        return request.env['website'].search([], limit=1)
        
    @http.route('/sh_product_snippet/get_products', type='json', auth="none", method = ['post'], website = True)
    def get_products(self, category_id = False, is_show_add_to_cart = False, is_show_product_desc = False, is_show_sale_price = False, is_show_wish_list = False, limit = False, order_by = False):

        
        if category_id and type(category_id) != int:
            category_id = int(category_id)
            
        product_order = "website_sequence desc,id desc"   
    
        if order_by == 'name_asc':
            product_order = "name asc"
        elif order_by == 'name_desc':
            product_order = "name desc"            
        
        elif order_by == 'create_date_asc':
            product_order = "create_date asc" 
        elif order_by == 'create_date_desc':
            product_order = "create_date desc" 
        
        elif order_by == 'sale_price_asc':
            product_order = "list_price asc" 
        elif order_by == 'sale_price_desc':
            product_order = "list_price desc" 
                                               

        if limit and type(limit) != int:
            limit = int(limit)
            
        product_domain = [
            ('sale_ok', '=', True),
            ('website_published', '=', True),
        ]
        
        if category_id:
            product_domain.append(('public_categ_ids','child_of',[category_id] ))        
        
        products =  request.env['product.template'].sudo().search(
            product_domain,
            order = product_order,
            limit = limit
            )
        
        
        data = """
      
 <div id="js_id_sh_product_snippet_div_row" class="row">

        """     
        if products:
            for product in products:
                 
                
                
                html = request.env.ref('sh_product_snippet.sh_product_snippet_products_item').render({
                    'product': product,
                    "product_href" : "/shop/product/%s" %(product.id),
                    'product_variant' : product._create_first_product_variant(),
                    'is_show_add_to_cart':is_show_add_to_cart,
                    'is_show_product_desc':is_show_product_desc,
                    'is_show_sale_price':is_show_sale_price,
                    'is_show_wish_list' :is_show_wish_list,
                    
                })
                
                data += html.decode("utf-8") 
       
                
        data += """
           </div>
            
        """
            
        return data
    
    
    
    
    
    
    
    
    
    
    @http.route('/sh_product_snippet/get_snippet_2_products', type='json', auth="none", method = ['post'], website = True)
    def get_snippet_2_products(self, category_id = False, is_show_add_to_cart = False, is_show_product_desc = False, is_show_sale_price = False, is_show_wish_list = False, limit = False, order_by = False):

        
        if category_id and type(category_id) != int:
            category_id = int(category_id)
            
        product_order = "website_sequence desc,id desc"   
    
        if order_by == 'name_asc':
            product_order = "name asc"
        elif order_by == 'name_desc':
            product_order = "name desc"            
        
        elif order_by == 'create_date_asc':
            product_order = "create_date asc" 
        elif order_by == 'create_date_desc':
            product_order = "create_date desc" 
        
        elif order_by == 'sale_price_asc':
            product_order = "list_price asc" 
        elif order_by == 'sale_price_desc':
            product_order = "list_price desc" 
                                               

        if limit and type(limit) != int:
            limit = int(limit)
            
        product_domain = [
            ('sale_ok', '=', True),
            ('website_published', '=', True),
        ]
        
        if category_id:
            product_domain.append(('public_categ_ids','child_of',[category_id] ))        
        
        products =  request.env['product.template'].sudo().search(
            product_domain,
            order = product_order,
            limit = limit
            )
        
        
        data = """
      
 <div id="js_id_sh_product_snippet_section_div_row_2" class="row">

        """     
        if products:
            for product in products:

                html = request.env.ref('sh_product_snippet.sh_product_snippet_products_item_2').render({
                    'product': product,
                    "product_href" : "/shop/product/%s" %(product.id),
                    'product_variant' : product._create_first_product_variant(),
                    'is_show_add_to_cart':is_show_add_to_cart,
                    'is_show_product_desc':is_show_product_desc,
                    'is_show_sale_price':is_show_sale_price,
                    'is_show_wish_list' :is_show_wish_list,
                    
                })
                
                data += html.decode("utf-8") 
       
                
        data += """
           </div>
            
        """
            
        return data    
    
    
    
    





    
    
    @http.route('/sh_product_snippet/get_snippet_3_products', type='json', auth="none", method = ['post'], website = True)
    def get_snippet_3_products(self, category_id = False, is_show_add_to_cart = False, is_show_product_desc = False, is_show_sale_price = False, is_show_wish_list = False, limit = False, order_by = False):

        
        if category_id and type(category_id) != int:
            category_id = int(category_id)
            
        product_order = "website_sequence desc,id desc"   
    
        if order_by == 'name_asc':
            product_order = "name asc"
        elif order_by == 'name_desc':
            product_order = "name desc"            
        
        elif order_by == 'create_date_asc':
            product_order = "create_date asc" 
        elif order_by == 'create_date_desc':
            product_order = "create_date desc" 
        
        elif order_by == 'sale_price_asc':
            product_order = "list_price asc" 
        elif order_by == 'sale_price_desc':
            product_order = "list_price desc" 
                                               

        if limit and type(limit) != int:
            limit = int(limit)
            
        product_domain = [
            ('sale_ok', '=', True),
            ('website_published', '=', True),
        ]
        
        if category_id:
            product_domain.append(('public_categ_ids','child_of',[category_id] ))        
        
        products =  request.env['product.template'].sudo().search(
            product_domain,
            order = product_order,
            limit = limit
            )
        
        
        data = """
      
 <div id="js_id_sh_product_snippet_section_div_row_3" class="row">

        """     
        if products:
            for product in products:
                 
                html = request.env.ref('sh_product_snippet.sh_product_snippet_products_item_3').render({
                    'product': product,
                    "product_href" : "/shop/product/%s" %(product.id),
                    'product_variant' : product._create_first_product_variant(),
                    'is_show_add_to_cart':is_show_add_to_cart,
                    'is_show_product_desc':is_show_product_desc,
                    'is_show_sale_price':is_show_sale_price,
                    'is_show_wish_list' :is_show_wish_list,
                    
                })
                
                data += html.decode("utf-8") 
       
                
        data += """
           </div>
            
        """
            
        return data  






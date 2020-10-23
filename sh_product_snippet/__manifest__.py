# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Dynamic Product Listing Snippets",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",  
    "category": "Website",
    "summary": """
   Product Snippet, Product Blocks, Product Snippets, Product Slider Snippet Module, Stylish Product Snippets, Goods Grid Block,Products Blocks App, Goods Snippet Application, Product Snipet, Product Box, Product Content Box, New Arrival Product Snippet, Featured Snippet, Alternative Product Snnipet, Category Wise Product, multiple Category products Odoo.
                    """,
    "description": """
This module provides a 3 different and stylish snippet for display products on the shop page. This snippet you can set in anywhere on the website so basically, you can use this snippet as the marketing of new arrival products as well as use for SEO. Easy to set products in the snippet as category wise. Also, you can set product description, add to cart and add to wish buttons, sale price.

   Product Snippet Odoo, Product Blocks Odoo
 Product Snippets, Product Slider Snippet Module, Stylish Product Snippets, Goods Grid Block,Products Blocks, Goods Snippet, Product Snipet, Product Box, Product Content Box, New Arrival Product Snippet, Featured Snippet, Alternative Product Snnipet, Category Wise Product, multiple Category products Odoo.
 Product Snippets, Product Slider Snippet Module, Stylish Product Snippets, Goods Grid Block,Products Blocks App, Goods Snippet Application, Product Snipet, Product Box, Product Content Box, New Arrival Product Snippet, Featured Snippet, Alternative Product Snnipet, Category Wise Product, multiple Category products Odoo.


                    """,    
    "version":"13.0.2",
    "depends" : ["base","website","website_sale","website_sale_wishlist"],
    "application" : True,
    "data" : [
                'views/snippets.xml',
                "views/product_item.xml",
                'views/assets.xml'
            ],     
           
    "images": ["static/description/background.png",], 
    "live_test_url": "https://www.youtube.com/watch?v=q6Y9Rd8-vJ4&feature=youtu.be",             
    "auto_install":False,
    "installable" : True,
    "price": 50,
    "currency": "EUR"   
}

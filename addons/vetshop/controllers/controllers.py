# from odoo import http


# class Vetshop(http.Controller):
#     @http.route('/vetshop/vetshop', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vetshop/vetshop/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vetshop.listing', {
#             'root': '/vetshop/vetshop',
#             'objects': http.request.env['vetshop.vetshop'].search([]),
#         })

#     @http.route('/vetshop/vetshop/objects/<model("vetshop.vetshop"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vetshop.object', {
#             'object': obj
#         })


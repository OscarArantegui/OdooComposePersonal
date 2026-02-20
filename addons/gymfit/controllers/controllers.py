# from odoo import http


# class Gymfit(http.Controller):
#     @http.route('/gymfit/gymfit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gymfit/gymfit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gymfit.listing', {
#             'root': '/gymfit/gymfit',
#             'objects': http.request.env['gymfit.gymfit'].search([]),
#         })

#     @http.route('/gymfit/gymfit/objects/<model("gymfit.gymfit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gymfit.object', {
#             'object': obj
#         })


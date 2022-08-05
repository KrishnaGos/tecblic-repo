# -*- coding: utf-8 -*-

#
# class ShopPage(http.Controller):
#
#     @http.route('/shope/academy/', auth='public')
#
#     # def index(self, **kw):
#     #     return "Hello, world"
#
#     def index(self, **kw):
#         return http.request.render('academy.index', {
#             'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
#         })
#
#     @http.route('/website/form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True,
#                 csrf=False)
#     def website_form(self, model_name, **kwargs):
#     # Partial CSRF check, only performed when session is authenticated, as there
#     # is no real risk for unauthenticated sessions
# -*- coding: utf-8 -*-
# from odoo import http


# class HmeAccount(http.Controller):
#     @http.route('/hme_account/hme_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hme_account/hme_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hme_account.listing', {
#             'root': '/hme_account/hme_account',
#             'objects': http.request.env['hme_account.hme_account'].search([]),
#         })

#     @http.route('/hme_account/hme_account/objects/<model("hme_account.hme_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hme_account.object', {
#             'object': obj
#         })

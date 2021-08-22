# -*- coding: utf-8 -*-
# from odoo import http


# class Hme14(http.Controller):
#     @http.route('/HME14/HME14/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/HME14/HME14/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('HME14.listing', {
#             'root': '/HME14/HME14',
#             'objects': http.request.env['HME14.HME14'].search([]),
#         })

#     @http.route('/HME14/HME14/objects/<model("HME14.HME14"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('HME14.object', {
#             'object': obj
#         })

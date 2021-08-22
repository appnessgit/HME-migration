# -*- coding: utf-8 -*-
from odoo import http

# class PurchaseHme(http.Controller):
#     @http.route('/hme_purchase/hme_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hme_purchase/hme_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hme_purchase.listing', {
#             'root': '/hme_purchase/hme_purchase',
#             'objects': http.request.env['hme_purchase.hme_purchase'].search([]),
#         })

#     @http.route('/hme_purchase/hme_purchase/objects/<model("hme_purchase.hme_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hme_purchase.object', {
#             'object': obj
#         })
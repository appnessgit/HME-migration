# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class hme_account(models.Model):
    _inherit = 'account.move.line'
    _description = 'obtain expiry date and batch number from sale order'
    
    # sale_order_fields = fields.Many2one(comodel_name='sale.order.line')
    expiry_date_invoice = fields.Datetime()
    batch_number_invoice = fields.Many2one('stock.production.lot')



    # @api.depends('sale_order_fields.order_line.batch_num')
    # def compute_batch_num(self):
    #     for rec in self:
    #         for lines in rec.sale_order_fields.order_line: 
    #             raise UserError(str(rec.batch_number_invoice))

    #             rec.batch_number_invoice=lines.batch_num
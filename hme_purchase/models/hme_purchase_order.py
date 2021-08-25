# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseHmeLine(models.Model):
    _inherit = "purchase.order"
    _description = 'Add purchase type field above vendor + Add terms of delivery field after receipt date fields+Add brand field at the beginning of the order line where it give list of brands. Once the brand has been chosen, when clicking on the product, it should give list of all the product that are related to that brand'
    purchase_type = fields.Selection(string='Purchase type', selection=[('import', 'Forign'), ('local', 'Local')], required=True)



class PurchaseHmeLine(models.Model):
    _inherit = "purchase.order.line"
    _description = 'Add brand field at the beginning of the order line where it give list of brands. Once the brand has been chosen, when clicking on the product, it should give list of all the product that are related to that brand'
    
    brand_id = fields.Many2one(comodel_name='res.partner', string="Brand" ,domain=[('is_brand','=',True)])
    product_id = fields.Many2one(comodel_name='product.product', string='Product')

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        return {'domain':{'product_id': [('brand_id','=',self.brand_id.id)]}}

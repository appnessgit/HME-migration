from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    name = fields.Char(readonly = False)
    brand_id = fields.Many2one('res.partner', string="Brand", domain=[('is_brand', '=', True)])
    batch_num = fields.Many2one('stock.production.lot', 'Batch Number')
    expiry_date = fields.Datetime('Expiry Date')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        return {'domain': {'product_id': [('brand_id', '=', self.brand_id.id)]}}


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    name = fields.Char(readonly = False)


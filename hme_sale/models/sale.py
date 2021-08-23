from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    brand_id = fields.Many2one('res.partner', string="Brand" ,domain=[('is_brand','=',True)])
    batch_num = fields.Many2one('stock.production.lot', 'Batch Number')
    expiry_date = fields.Datetime('Expiry Date')
    # product_id = fields.Many2one('product.template', string='Product', change_default=True, ondelete='restrict',
    #                              required=True)
    #


class SaleOrder(models.Model):
    _inherit = "sale.order"


    # purchase_order_count = fields.Integer()
    warehouse_id=fields.Boolean()

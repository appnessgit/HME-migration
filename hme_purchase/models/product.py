from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand_id = fields.Many2one('res.partner', string="Brand")
    type_id = fields.Many2one('product.type', string='Type')
    default_code = fields.Char('Code')
    service_to_purchase=fields.Boolean()


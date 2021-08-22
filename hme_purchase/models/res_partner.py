

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_brand = fields.Boolean(string="Is a Brand")
    product_ids = fields.One2many('product.template','brand_id')
    product_count = fields.Integer(compute="_compute_products")

    def _compute_products(self):
        for rec in self:
            rec.product_count = len(rec.product_ids)

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        for partner in self:
            if partner.is_brand== True:
                partner.company_type = 'brand_id'



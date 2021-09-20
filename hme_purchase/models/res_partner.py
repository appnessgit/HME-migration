from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_brand = fields.Boolean(string="Is a Brand")
    is_vendor = fields.Boolean(string="Is a Vendor")
    product_ids = fields.One2many('product.template', 'brand_id')
    product_count = fields.Integer(compute="_compute_products")
    vendor_type = fields.Selection(string='Vendor Type', selection=[('import', 'Forign'), ('local', 'Local')])
    customer_type = fields.Many2one('customer.type', string="Customer Type")

    def _compute_products(self):
        for rec in self:
            rec.product_count = len(rec.product_ids)

    def action_view_product(self):
        for rec in self:
            return {
                'name': _('product'),
                'view_mode': 'tree,form',
                'res_model': 'product.template',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [('brand_id', '=', self.id)],

            }

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        for partner in self:
            if partner.is_brand == True:
                partner.company_type = 'brand_id'


class CustomerType(models.Model):
    _name = "customer.type"
    name = fields.Char(string='Customer Type')

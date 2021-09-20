
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Stock(models.Model):
    _inherit = 'stock.move'
    brand_id = fields.Many2one(comodel_name='res.partner', string="Brand" ,domain=[('is_brand','=',True)])
    product_id = fields.Many2one(comodel_name='product.product', string='Product')

    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        return {'domain': {'product_id': [('brand_id', '=', self.brand_id.id)]}}

                                                  
    
class Stock_picking(models.Model):
    _inherit = 'stock.picking'
    purchase_type = fields.Selection(related='purchase_id.purchase_type')
    
    # def compute_can_edit(self):
    #     self.purchase_type = self.purchase_id.purchase_type
            
    

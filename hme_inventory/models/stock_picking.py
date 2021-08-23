from odoo import api, fields, models


class Stock(models.Model):
    _inherit = 'stock.move'
    pack_operation_product_ids = fields.Many2one(comodel_name='res.partner', string='brand')
                                                  
    
        
    

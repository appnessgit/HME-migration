from odoo import api, fields, models

class product_p(models.Model):
    _inherit = 'product.product'
   
    bool_can_edit = fields.Boolean('Edit' , compute="compute_can_edit")

    def compute_can_edit(self):
        for record in self: 
          if self.env.user.has_group('stock.group_stock_manager'):
            record.bool_can_edit = True
          else:
            record.bool_can_edit = False

        
  

    # @api.onchange("lst_price")
    # def _compute_can_edit(self):
    #     if self.env.user.has_group('stock.group_stock_manager'):
    #         pass
    #     else:
    #         raise UserWarning("You're incapabble of ")

    
        
    

    

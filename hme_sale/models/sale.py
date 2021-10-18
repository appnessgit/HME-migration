from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    name = fields.Char(readonly = False)
    brand_id = fields.Many2one('res.partner', string="Brand", domain=[('is_brand', '=', True)])
    batch_num = fields.Many2one('stock.production.lot', 'Batch Number')
    expiry_date = fields.Datetime('Expiry Date')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0, readonly=True)
    # q = {'batch_number_invoice': batch_num,'expiry_date_invoice': expiry_date,}



# Thi function is from odoo's ase module: sale / model: sale.order.line which is called when user creates a REGULAR invoice. This function is called and passed the customized fields
# called batch number and expiry date to hav them be visible when an invoice is created //account.move.line
    def _prepare_invoice_line(self, **optional_values):
        # self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        # raise UserError(self.batch_num.name)
        # res.update(optional_values=self.q)
        res['batch_number_invoice'] = self.batch_num.id
        res['expiry_date_invoice'] = self.expiry_date
        return res
   
   
   
   
   
   
   
    # def pass_batch_num(self):

    # qty = {
    # 'batch_number_invoice': self.batch_num,
    # 'expiry_date_invoice': self.expiry_date,
    #     }
    # raise UserError(optional_values_2)
    # super(SaleOrderLine, self)._prepare_invoice_line(self,optional_values_2)
    # self._prepare_invoice_line(self,optional_values)
    # raise UserError("uhljk;")
    # return rec

    # def _prepare_invoice_line(self, **optional_values):
    #     """
    #     Prepare the dict of values to create the new invoice line for a sales order line.

    #     :param qty: float quantity to invoice
    #     :param optional_values: any parameter that should be added to the returned invoice line
    #     """
    #     self.ensure_one()
    #     res = {
    #         'display_type': self.display_type,
    #         'sequence': self.sequence,
    #         'name': self.name,
    #         'product_id': self.product_id.id,
    #         'product_uom_id': self.product_uom.id,
    #         'quantity': self.qty_to_invoice,
    #         'discount': self.discount,
    #         'price_unit': self.price_unit,
    #         'tax_ids': [(6, 0, self.tax_id.ids)],
    #         'analytic_account_id': self.order_id.analytic_account_id.id,
    #         'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
    #         'sale_line_ids': [(4, self.id)],
    #         'batch_number_invoice': self.batch_num,
    #         'expiry_date_invoice': self.expiry_date,

    #     }
    #     if optional_values:
    #         res.update(optional_values)
    #     if self.display_type:
    #         res['account_id'] = False
    #     return res


    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        return {'domain': {'product_id': [('brand_id', '=', self.brand_id.id)]}}


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    name = fields.Char(readonly = False)


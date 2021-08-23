from odoo import api, fields, models


class Crminherited(models.Model):
    _inherit = 'mail.activity'
    # user_id =fields.Many2many(relation='res.users', string='Assigned to')
    user_ids = fields.Many2many(comodel_name='res.users', string='Assigned to')
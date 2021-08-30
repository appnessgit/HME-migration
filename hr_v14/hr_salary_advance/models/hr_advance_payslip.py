# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields
from odoo.exceptions import UserError


class SalaryRuleInput(models.Model):
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(SalaryRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids[0].id).employee_id
        adv_salary = self.env['salary.advance'].search([('employee_id', '=', emp_id.id)])
        for adv_obj in adv_salary:
            current_date = date_from.month
            date = adv_obj.date
            existing_date = date.month
            if current_date == existing_date:
                state = adv_obj.state
                amount = adv_obj.advance
                for result in res:
                    if state == 'approve' and amount != 0 and result.get('code') == 'SAR':
                        result['amount'] = amount
        return res

    salary_advance = fields.Float(string="Salary Advance")

    def get_salary_advance(self):
        for payslip in self:
            contract_obj = self.env['hr.contract']
            emp_id = payslip.employee_id
            adv_salary = self.env['salary.advance'].search([
                ('employee_id', '=', self.employee_id.id),
                ('state', '=', 'approve'),
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to)
            ])
            amount = 0
            for adv in adv_salary:
                amount += adv.advance

            payslip.salary_advance = amount


    def compute_sheet(self):
        self.get_salary_advance()
        super(SalaryRuleInput, self).compute_sheet()




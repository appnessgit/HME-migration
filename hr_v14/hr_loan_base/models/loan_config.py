from openerp import models, fields, api , _
from openerp.exceptions import except_orm, Warning, RedirectWarning, UserError

class hr_loan_config(models.Model):
	_name = 'hr.loan.config'

	name = fields.Char("Loan Name")
	payroll_code = fields.Char("Payroll Code")
	description = fields.Text("Description")
	condition = fields.Selection([('always','Always'),('formula','Formula')], string="Condition", required=True)
	date = fields.Date("Date")
	amount = fields.Float("Amount")
	number = fields.Integer("Number")
	join_date_comparison = fields.Selection([('number', 'Number Of Month'),('date', 'Date')])
	interval_base = fields.Selection([('year', 'Year'), ('month', 'Month')])
	sign = fields.Selection([('greater','>'),('less','<'),('equal','='),('greater_equal','>='),('less_equal','=<')])
	employee_request = fields.Boolean("Request By Employee", default=True)
	maximum_month_gross = fields.Integer("Maximum Amount (Gross Month)")
	installment = fields.Integer("number of Installment")
	set_no_of_installmens = fields.Boolean(string='Set number of installments')
	max_base = fields.Selection([('fixed','Fixed Amount'),('gross_month','Gross month')], string="Maximum Amount Based")

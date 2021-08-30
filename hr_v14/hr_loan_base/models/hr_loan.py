from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class hr_loan(models.Model):
	_name = 'hr.loan'
	_inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']
	_description = "HR Loan Request"

	def unlink(self):
		for rec in self:
			if rec.state != "draft":
				raise UserError("Sorry, only DRAFT Loans can be deleted.")
			else:
				res = super(hr_loan, rec).unlink()
				return res

	def _compute_amount(self):
		for loan in self:
			total_paid_amount = 0.00
			for line in loan.loan_line_ids:
				if line.paid == True:
					total_paid_amount += line.paid_amount

			balance_amount = loan.loan_amount - total_paid_amount
			loan.total_amount = loan.loan_amount
			loan.balance_amount = balance_amount
			loan.total_paid_amount = total_paid_amount

	def _get_old_loan(self):
		old_amount = 0.00
		for loan in self.search([('employee_id', '=', self.employee_id.id)]):
			if loan.id != self.id:
				old_amount += loan.balance_amount
		self.loan_old_amount = old_amount

	@api.depends('total_amount', 'total_paid_amount', 'loan_line_ids.paid')
	def comp_progress(self):
		for rec in self:
			if rec.total_amount and rec.total_paid_amount != 0.0:
				rec.progress = (rec.total_paid_amount/rec.total_amount)*100
			else:
				rec.progress = 0.0

	def _default_employee(self):
		return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

	active = fields.Boolean("active", default=True)
	name = fields.Char(string="Loan Name", default="/", readonly=True)
	date = fields.Date(string="Date Request",default=fields.Date.today(), readonly=True)
	employee_id = fields.Many2one('hr.employee', string="Employee", required=True, default=_default_employee)
	image = fields.Binary(related="employee_id.image_1920")
	parent_id = fields.Many2one('hr.employee', related="employee_id.parent_id", string="Manager")
	department_id = fields.Char(related="employee_id.department_id.name", readonly=True, string="Department", store=True)
	job_id = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position")
	emp_salary = fields.Float(string="Employee Salary")
	loan_old_amount = fields.Float(string="Old Loan Amount Not Paid", compute='_get_old_loan')
	loan_amount = fields.Float(string="Loan Amount", required=True)
	total_amount = fields.Float(string="Total Amount", readonly=True, compute='_compute_amount')
	balance_amount = fields.Float(string="Remaining Amount", compute='_compute_amount')
	total_paid_amount = fields.Float(string="Total Paid Amount", compute='_compute_amount')
	progress = fields.Float(string="Progress %",compute=comp_progress, readonly=True, store=True)
	color = fields.Integer(string='Color Index')
	no_month = fields.Integer(string="No Of Month")
	# no_month = fields.Integer(string="No Of Month", default=1)
	payment_start_date = fields.Date(string="Start Date of Payment", required=True, default=fields.Date.today())
	loan_line_ids = fields.One2many('hr.loan.line', 'loan_id', string="Loan Line", index=True)
	loan_config_id = fields.Many2one(comodel_name='hr.loan.config', string='Loan Type', required=True, )
	  

	state = fields.Selection([
		('draft', 'Draft'),
		('hr_approve', 'HR Manager Approve'),
		('approve', 'Approved'),
		('refuse', 'Refused'),
	], string="State", default='draft', track_visibility='onchange', copy=False)

	@api.constrains('loan_config_id')
	def onchange_loan_config_id(self):
		if self.loan_config_id:
			if (not self.loan_config_id.employee_request) and (not self.env.user.has_group('hr.group_hr_user')):
				raise UserError(_("This Loan Type Should Be Created By HR Only"))

		if self.loan_config_id.condition == 'formula':

			emp_join_date = self.sudo().employee_id.contract_id.date_start

			# Date
			if self.loan_config_id.join_date_comparison == 'date':
				if self.loan_config_id.sign == 'greater' and not (self.loan_config_id.date < emp_join_date):
					raise UserError(
						_("The date in Loan Type Condition Greater than Joining Date"))

				elif self.loan_config_id.sign == 'less' and not (self.loan_config_id.date > emp_join_date):
					raise UserError(
						_("The date in Loan Type Condition less than Joining Date"))

				elif self.loan_config_id.sign == 'equal' and self.loan_config_id.date != emp_join_date:
					raise UserError(
						_("The Joining Date of employee Not Equal the date in Loan Type Condition"))

				elif self.loan_config_id.sign == 'greater_equal' and self.loan_config_id.date > emp_join_date:
					raise UserError(
						_("The Condition in loan Type  Not realized"))

				elif self.loan_config_id.sign == 'less_equal' and self.loan_config_id.date < emp_join_date:
					raise UserError(
						_("The Joining Date of employee Greater the date in Loan Type Condition"))

			# Number
			elif self.loan_config_id.join_date_comparison == 'number':
				date_today = datetime.now().date()
				date_join = emp_join_date
				diff = relativedelta(date_today, date_join)
				# Year
				if self.loan_config_id.interval_base == 'year':
					if diff.years:
						years = diff.years
					else:
						years = 0
					if self.loan_config_id.sign == 'greater' and not (self.loan_config_id.number < years):
						raise UserError(
							_("Your work years should be more than the years of this loan type"))

					elif self.loan_config_id.sign == 'less' and not (self.loan_config_id.number > years):
						raise UserError(
							_("Your work years should be less than the years of this loan type"))

					elif self.loan_config_id.sign == 'equal' and self.loan_config_id.number != years:
						raise UserError(
							_("Your work years should be equal to the years of this loan type"))

					elif self.loan_config_id.sign == 'greater_equal' and self.loan_config_id.number > years:
						raise UserError(
							_("Your work years should be more than or equal to the years of this loan type"))

					elif self.loan_config_id.sign == 'less_equal' and self.loan_config_id.number < years:
						raise UserError(
							_("Your work years should be less than or equal to the years of this loan type"))
				# Month
				else:
					if diff.months:
						if diff.years:
							months = diff.months+(12*diff.years)
						else:
							months = diff.months
					else:
						if diff.years:
							months = 12*diff.years
						else:
							months = 0
					if self.loan_config_id.sign == 'greater' and not (self.loan_config_id.number < months):
						raise UserError(
							_("Your work months should be more than the months of this loan type"))

					elif self.loan_config_id.sign == 'less' and not (self.loan_config_id.number > months):
						raise UserError(
							_("Your work months should be less than the months of this loan type"))

					elif self.loan_config_id.sign == 'equal' and self.loan_config_id.number != months:
						raise UserError(
							_("Your work months should be equal to the months of this loan type"))

					elif self.loan_config_id.sign == 'greater_equal' and self.loan_config_id.number > months:
						raise UserError(
							_("Your work months should be more than or equal to the months of this loan type"))

					elif self.loan_config_id.sign == 'less_equal' and self.loan_config_id.number < months:
						raise UserError(
							_("Your work months should be less than or equal to the months of this loan type"))

		if self.loan_config_id.max_base == 'fixed':
			if self.loan_amount:
				if self.loan_config_id.amount == 0 or self.loan_amount <= self.loan_config_id.amount:
					pass
				else:
					raise UserError('Loan Amount Exceeded the Maximum Amount')
		elif self.loan_config_id.max_base == 'gross_month' :
			x = self.loan_config_id.maximum_month_gross * self.sudo().employee_id.contract_id.wage
			if self.loan_amount > x:
				raise UserError('Loan Amount Exceeded the Maximum Amount')
		else:
			pass
		self.no_month = self.loan_config_id.installment if self.loan_config_id.set_no_of_installmens else 1 
		self.compute_loan_line()

	@api.onchange('loan_amount')
	def _onchange_loan_amount(self):
		self.onchange_loan_config_id()

	@api.onchange('loan_config_id')
	def _onchange_loan_config(self):
		self.onchange_loan_config_id()

	@api.constrains('no_month')
	def _check_no_month(self):
		if self.no_month == 0:
			self.no_month = 1
		
	@api.onchange('employee_id')
	def _onchange_employee_id(self):
		for rec in self:
			if rec.sudo().employee_id.contract_id:
				rec.emp_salary = rec.sudo().employee_id.contract_id.wage

	@api.model
	def create(self, values):
		values['name'] = self.env['ir.sequence'].get('hr.loan.req') or ' '
		res = super(hr_loan, self).create(values)
		return res
	
	def action_submit(self):
		for rec in self:
			hr_manager_user = []
			hr_manager_user = rec.env.ref('hr.group_hr_manager').users
			for manager_user in hr_manager_user:
				rec.activity_unlink(['hr_loan_base.mail_loan_request'])
				rec.activity_schedule('hr_loan_base.mail_loan_request', user_id=manager_user.id)
			rec.state = 'hr_approve'
		
	def action_refuse(self):
		for rec in self:
			rec.activity_unlink(['hr_loan_base.mail_loan_request'])
			rec.state = 'refuse'

	def action_set_to_draft(self):
		self.state = 'draft'

	def onchange_employee_id(self, employee_id=False):
		old_amount = 0.00
		if employee_id:
			for loan in self.search([('employee_id', '=', employee_id)]):
				if loan.id != self.id:
					old_amount += loan.balance_amount
			return {
				'value': {
					'loan_old_amount': old_amount}
			}

	def action_approve(self):
		for rec in self:
			rec.state = 'approve'
			rec.activity_unlink(['hr_loan_base.mail_loan_request'])
		return True

	def compute_loan_line(self):
		# self.onchange_loan_config_id()
		loan_line = self.env['hr.loan.line']
		loan_line.search([('loan_id', '=', self.id)])
		lines = [(5, 0, 0)]
		for loan in self:
			date_start = loan.payment_start_date
			counter = 1
			amount_per_time = loan.loan_amount / loan.no_month
			for i in range(1, loan.no_month + 1):
				line_id = {
					'paid_date': date_start,
					'paid_amount': amount_per_time,
					'employee_id': loan.employee_id.id,
					'loan_id': loan.id}
				lines.append((0, 0, line_id))
				loan.loan_line_ids = lines
				counter += 1
				date_start = date_start + relativedelta(months=1)
		return True

	def button_reset_balance_total(self):
		total_paid_amount = 0.00
		for loan in self:
			for line in loan.loan_line_ids:
				if line.paid == True:
					total_paid_amount += line.paid_amount
			balance_amount = loan.loan_amount - total_paid_amount
			self.write({'total_paid_amount': total_paid_amount,
						'balance_amount': balance_amount})


class hr_loan_line(models.Model):
	_name = "hr.loan.line"
	_description = "HR Loan Request Line"

	paid_date = fields.Date(string="Payment Date", required=True)
	employee_id = fields.Many2one('hr.employee', string="Employee")
	paid_amount = fields.Float(string="Paid Amount", required=True)
	paid = fields.Boolean(string="Paid")
	notes = fields.Text(string="Notes")
	loan_id = fields.Many2one(
		'hr.loan', string="Loan Ref.", ondelete='cascade')
	payroll_id = fields.Many2one('hr.payslip', string="Payslip Ref.")
	active = fields.Boolean(related="loan_id.active")
	state = fields.Selection(related="loan_id.state", store=True)

	def action_unpaid(self):
		if self.loan_id.active == False:
			raise UserError(
				_('Warning', "Loan Request must be approved and active"))
			return False
		else:
			self.paid = False
			return True

	def action_paid_amount(self):
		if self.loan_id.active == False:
			self.action_unpaid()
			return False
		context = self._context
		can_close = False
		loan_obj = self.env['hr.loan']
		created_move_ids = []
		loan_ids = []
		for line in self:
			if line.loan_id.state != 'approve':
				raise except_orm("Loan Request must be approved")
			paid_date = line.paid_date
			amount = line.paid_amount
			loan_name = line.employee_id.name
			reference = line.loan_id.name
		return True


class hr_employee(models.Model):
	_inherit = "hr.employee"

	@api.model
	def _compute_loans(self):
		for rec in self:
			count = 0
			loan_remain_amount = 0.00
			loan_ids = self.env['hr.loan'].search(
				[('employee_id', '=', rec.id)])
			for loan in loan_ids:
				loan_remain_amount += loan.balance_amount
				count += 1
			rec.loan_count = count
			rec.loan_amount = loan_remain_amount

	loan_amount = fields.Float(string="loan Amount", compute='_compute_loans')
	loan_count = fields.Integer(string="Loan Count", compute='_compute_loans')

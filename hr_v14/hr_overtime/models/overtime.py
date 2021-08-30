# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError, ValidationError
import json


class Overtime(models.Model):
    _name='hr.over.time'
    _description = "Overtime"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'


    @api.depends("hours_holiday")
    def comp_holiday_hours(self):
        self.calculated_holiday_hours = self.hours_holiday * self.company_id.hours_holiday_rate


    @api.depends("hours_weekend")
    def comp_weekend_hours(self):
        self.calculated_weekend_hours = self.hours_weekend * self.company_id.hours_weekend_rate


    @api.depends("hours_normal")
    def comp_normal_hours(self):
        self.calculated_day_hours = self.hours_normal * self.company_id.hours_normal_rate


    @api.depends("hours_night")
    def comp_night_hours(self):
        self.calculated_night_hours = self.hours_night * self.company_id.hours_night_rate


    @api.depends('calculated_holiday_hours', 'calculated_day_hours', 'calculated_night_hours', 'calculated_weekend_hours')
    def comp_total(self):
        self.total = self.calculated_holiday_hours + self.calculated_day_hours + self.calculated_night_hours + self.calculated_weekend_hours



	# Calculating The Overtimes For Each Category	
    @api.depends('total', 'gross_salary', 'basic_salary', 'calculated_day_hours', 'calculated_night_hours', 'calculated_weekend_hours', 'calculated_holiday_hours')
    def comp_overtime(self):
        hours_per_day = self.sudo().employee_id.resource_calendar_id.hours_per_day if self.employee_id.resource_calendar_id else 1
        # raise UserError(hours_per_day)
        normal_salary = self.basic_salary if self.company_id.normal_rate_salary == 'basic' else self.gross_salary
        night_salary = self.basic_salary if self.company_id.night_rate_salary == 'basic' else self.gross_salary
        weekend_salary = self.basic_salary if self.company_id.weekend_rate_salary == 'basic' else self.gross_salary
        holiday_salary = self.basic_salary if self.company_id.holiday_rate_salary == 'basic' else self.gross_salary
        # hours_per_day = self.hours_per_day

        self.overtime_normal = ((normal_salary / 30 / hours_per_day) * self.calculated_day_hours)
        self.overtime_night = ((night_salary / 30 / hours_per_day) * self.calculated_night_hours)
        self.overtime_weekend = ((weekend_salary / 30 / hours_per_day) * self.calculated_weekend_hours)
        self.overtime_holiday = ((holiday_salary / 30 / hours_per_day) * self.calculated_holiday_hours)
        self.overtime = self.overtime_normal + self.overtime_night + self.overtime_weekend + self.overtime_holiday


    # Net of All Overtime
    @api.depends('overtime')
    def comp_Net_overtime(self):
        self.net_overtime = self.overtime


    @api.depends('employee_id','date')
    def comp_gross_salary(self):
        if self.employee_id:
            if not self.env['hr.employee'].sudo().browse(self.employee_id.id).contract_id :
                self.gross_salary = 0.0
            else:
                self.gross_salary = self.sudo().employee_id.contract_id.wage
        else:
            pass


    @api.depends('employee_id')
    def comp_basic_salary(self):
        if self.employee_id:
            if not self.env['hr.employee'].sudo().browse(self.employee_id.id).contract_id :
                self.basic_salary=0.0
            else:
                self.basic_salary = self.sudo().employee_id.contract_id.basic
        else:
            pass

    # _sql_constraints = [
    #     ('unique_date_employee_id', 'UNIQUE(date,employee_id)', "Overtime: a record with the same date and employee already exists!"),]

    @api.constrains('hours_normal')
    def check_hours_normal(self):
        if self.hours_normal < 0:
            raise ValidationError('Normal hours Number must be greater than 0')

    @api.constrains('hours_holiday')
    def check_hours_holiday(self):
        if self.hours_holiday < 0:
            raise ValidationError('Holidays hours Number must be greater than 0')

    @api.constrains('other_amount')
    def check_other_amount(self):
        if self.other_amount < 0:
            raise ValidationError('Other Amount must be greater than 0')

    @api.constrains('weekend_amount')
    def check_weekend_amount(self):
        if self.weekend_amount < 0:
            raise ValidationError('Weekend Amount must be greater than 0')

    # def _default_employee(self):
    #     return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    # Fields
    state = fields.Selection([
        ('draft', 'Draft'),
        ('hr_officer', 'HR Officer Approval'),
        ('hrm_approval', 'HR Manager Approval'),
        ('confirm', 'Confirmed'),
        ('cancel', "Canceled"),
        ('reject', 'Rejected')
    ], string="State", default='draft', track_visibility='onchange', copy=False)

    employee_id = fields.Many2one('hr.employee', string="Employee",required=True)
    gross_salary=fields.Float("Gross Salary",compute=comp_gross_salary,store=True)
    basic_salary=fields.Float("Basic Salary",compute=comp_basic_salary,store=True)
    department_id=fields.Many2one("hr.department",string="Department",related="employee_id.department_id",readonly=False,store=True)
    date = fields.Date("Overtime Date", required=True,readonly=False,copy=False,default=time.strftime('%Y-%m-%d'))
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,default=lambda self: self.env['res.company']._company_default_get('hr.over.time'))
    note = fields.Text('Remarks')
    hours_per_day = fields.Float("Hours Per Day", compute='compute_hours_per_days')

    hours_holiday=fields.Float(string="Holidays Days")
    hours_normal = fields.Float(string="Normal hours")
    hours_night = fields.Float("Night Hours")
    hours_weekend = fields.Float("Weekend Hours")

    calculated_day_hours=fields.Float(string="Calculated Day Hours",compute=comp_normal_hours,store=True, readonly=True)
    calculated_holiday_hours=fields.Float(string="Calculated Holiday Hours",compute=comp_holiday_hours,store=True)
    calculated_night_hours=fields.Float(string="Calculated Night Hours",compute=comp_night_hours,store=True)
    calculated_weekend_hours=fields.Float(string="Calculated Weekend Hours",compute=comp_weekend_hours,store=True)

    # Rates
    hours_normal_rate=fields.Float(string="Day Hours Rate",related='company_id.hours_normal_rate')
    hours_holiday_rate=fields.Float(string="Holiday Rate",related='company_id.hours_holiday_rate')
    hours_night_rate=fields.Float(string="Night Hours Rate ",related='company_id.hours_night_rate')
    hours_weekend_rate=fields.Float(string="Weekend Hours Rate",related='company_id.hours_weekend_rate')


    total=fields.Float(string="Total hours",compute=comp_total,store=True)

    overtime=fields.Float(string="Overtime Total amount",compute=comp_overtime,store=True)
    overtime_normal=fields.Float(string="Overtime Total amount",compute=comp_overtime,store=True)
    overtime_night=fields.Float(string="Overtime Total amount",compute=comp_overtime,store=True)
    overtime_weekend=fields.Float(string="Overtime Total amount",compute=comp_overtime,store=True)
    overtime_holiday=fields.Float(string="Overtime Total amount",compute=comp_overtime,store=True)

    net_overtime=fields.Float(string="Net Overtime",compute=comp_Net_overtime,store=True)


    @api.onchange('day_hours_from','day_hours_to','night_hours_from','night_hours_to','holiday_from','holiday_to','weekday_from','weekday_to')
    def onchange_overtime_datetime(self):
        for rec in self:
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            if rec.day_hours_from and rec.day_hours_to:
                date_from = datetime.strptime(str(rec.day_hours_from), DATETIME_FORMAT)
                date_to = datetime.strptime(str(rec.day_hours_to), DATETIME_FORMAT)
                rec.hours_normal = abs((date_to - date_from).total_seconds() / 3600.0)
            if rec.night_hours_from and rec.night_hours_to:
                date_from = datetime.strptime(str(rec.night_hours_from), DATETIME_FORMAT)
                date_to = datetime.strptime(str(rec.night_hours_to), DATETIME_FORMAT)
                rec.hours_night = abs((date_to - date_from).total_seconds() / 3600.0)
            if rec.holiday_from and rec.holiday_to:
                date_from = datetime.strptime(str(rec.holiday_from), DATETIME_FORMAT)
                date_to = datetime.strptime(str(rec.holiday_to), DATETIME_FORMAT)
                rec.hours_holiday = abs((date_to - date_from).days) + 1
            if rec.weekday_from and rec.weekday_to:
                date_from = datetime.strptime(str(rec.weekday_from), DATETIME_FORMAT)
                date_to = datetime.strptime(str(rec.weekday_to), DATETIME_FORMAT)
                rec.hours_weekend = abs((date_to - date_from).days) + 1

    @api.depends('employee_id')
    def compute_hours_per_days(self):
        if self.employee_id:
            if self.sudo().employee_id.resource_calendar_id:
                # raise UserError(self.sudo().employee_id.resource_calendar_id.hours_per_day)
                self.hours_per_days = self.sudo().employee_id.resource_calendar_id.hours_per_day
            else:
                self.hours_per_days = 0
        else:
            pass


    # Create Function
    @api.model
    def create(self, vals):
        result = super(Overtime, self).create(vals)
        employee = result.employee_id
        line_manager = result.employee_id.line_manager_id
        current_user = self.env.user.employee_id
        if self.env.user.has_group('hr.group_hr_user') or employee.id == current_user.id or line_manager.id == current_user.id:
            return result
        else:
            raise UserError('You Are Not Allowed To Create Overtime For Other Employees')


    # Write Function
    # def write(self, vals):
    #     res = super(Overtime,self).write(vals)
    #     employee = self.employee_id
    #     line_manager = employee.employee_id.line_manager_id
    #     current_user = self.env.user.employee_id
    #     if self.env.user.has_group('hr.group_hr_user') or employee.id == current_user.id or line_manager.id == current_user.id:
    #         return res
    #     else:
    #         raise UserError('You Are Not Allowed To Change Overtime For Other Employees')

    def update_activities(self):
        for rec in self:
            users = []
            if rec.state not in ['draft','hr_officer','hrm_approval','confirm','cancel']:
                continue
            message = ""

            if rec.state == 'hr_officer':
                users = self.env.ref('hr.group_hr_user').users
                message = "Approve"

            if rec.state == 'hr_approval':
                users = self.env.ref('hr.group_hr_manager').users
                message = "Approve"


            elif rec.state == 'cancel':
                users = [self.create_uid]
                message = "Rejected"
            for user in users:
                self.activity_schedule('hr_overtime.mail_act_approval', user_id=user.id, note=message)

    #submit function
    def button_submit(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = "hr_officer"
            else:
                raise UserError("You have record not in Draft state")
            rec.update_activities()

    def button_hr_officer_approval(self):
        for rec in self:
            if rec.state == 'hr_officer':
                rec.state = "hrm_approval"
            else:
                raise UserError("You have record not in HR Officer state")

            rec.update_activities()



    #HRM Approve Function
    def button_hr_manager_approval(self):
        for rec in self:
            if rec.state == 'hrm_approval':
                rec.state = "confirm"
            else:
                raise UserError("You have record not in HRM state")
            rec.activity_unlink(['hr_overtime.mail_act_approval'])

    def action_reject(self):
        for rec in self:
            rec.state = 'reject'
            email = rec.employee_id.work_email
            mail_content = "  Hello  "  ",<br> Your Overtime request was rejected from your manager, please contact your manager for clarification."
            main_content = {
                'subject': 'Overtime Request',
                'author_id': rec.env.user.partner_id.id,
                'body_html': mail_content,
                'email_to': email,
            }
            rec.env['mail.mail'].sudo().create(main_content).send()
            rec.update_activities()


    #Cancell Function
    def button_cancel(self):
        for rec in self:
           rec.state = "cancel"

    #Draft Function
    def button_set_draft(self):
        for rec in self:
            rec.state = "draft"

    #Unlink Function
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError("You cannot delete this OverTime. Only DRAFT Requests can be deleted.")
            return super(Overtime, self).unlink()




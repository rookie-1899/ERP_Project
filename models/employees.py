# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HRManagement(models.Model):
    _name = 'salesman.employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'HR'
    _rec_name = 'employee_name'
    _order = 'id desc'

    employee_seq = fields.Char(string='Mã Nhân Viên', required=True, copy=False, readonly=True,
                               index=True, default=lambda self: _('New'))
    employee_name = fields.Char(string='Tên Nhân Viên', required=True, track_visibility="always")
    employee_group = fields.Selection([
        ('bếp', 'Bếp'),
        ('pha chế', 'Pha Chế'),
        ('phục vụ', 'Phục Vụ'),
    ], string='Bộ Phận', required=True, track_visibility="always")
    employee_status = fields.Selection([
        ('part time', 'Part Time'),
        ('full time', 'Full Time'),
    ], string='Làm Việc', required=True, track_visibility="always")
    employee_salary = fields.Float(string='Lương Cơ Bản', required=True, track_visibility="always")
    employee_date = fields.Date(string="Ngày Tạo", required="True",
                                default=lambda self: fields.Date.today(), readonly=True)
    notes = fields.Text(string="Ghi Chú")

    employee_group_store = fields.Char(string='Tên Bộ Phận')
    employee_status_store = fields.Char(string='Trạng Thái Làm Việc')

    # create sequence for NVL
    @api.model
    def create(self, vals):
        if vals.get('employee_seq', _('New')) == _('New'):
            vals['employee_seq'] = self.env['ir.sequence'].next_by_code('salesman.employee.sequence') or _('New')
        result = super(HRManagement, self).create(vals)
        return result

    # create sequence for NVL
    @api.onchange('employee_group')
    def set_employee_group(self):
        for rec in self:
            if rec.employee_group:
                if rec.employee_group == 'bếp' or rec.employee_group == 'Bếp':
                    rec.employee_group_store = 'Bếp'
                    print('something', rec.employee_group_store)
                elif rec.employee_group == 'pha chế' or rec.employee_group == 'Pha Chế':
                    rec.employee_group_store = 'Pha Chế'
                    print('something', rec.employee_group_store)
                else:
                    rec.employee_group_store = 'Phục Vụ'
                    print('something', rec.employee_group_store)

    # create sequence for NVL
    @api.onchange('employee_status')
    def set_employee_status(self):
        for rec in self:
            if rec.employee_status:
                if rec.employee_status == 'part time' or rec.employee_status == 'Part Time':
                    rec.employee_status_store = 'Part Time'
                    print('something', rec.employee_status_store)
                else:
                    rec.employee_status_store = 'Full Time'
                    print('something', rec.employee_status_store)


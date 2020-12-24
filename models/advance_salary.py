# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HRAdvanceSalary(models.Model):
    _name = 'salesman.advance.salary'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Advance Salary'
    _rec_name = 'record_date'
    _order = 'record_date desc'

    advance_salary_record_seq = fields.Char(string='Mã Nhân Viên', required=True, copy=False, readonly=True,
                                            index=True, default=lambda self: _('New'))
    record_date = fields.Date(string="Ngày Tạo", required="True",
                              default=lambda self: fields.Date.today(), readonly=True)
    notes = fields.Text(string="Ghi Chú")
    employee_record = fields.One2many(comodel_name="salesman.advance.salary.record", inverse_name="doc_id", string="Thêm NV")

    # employee_name = fields.Char(string='Tên Nhân Viên', required=True, track_visibility="always")
    # employee_group = fields.Selection([
    #     ('bếp', 'Bếp'),
    #     ('pha chế', 'Pha Chế'),
    #     ('phục vụ', 'Phục Vụ'),
    # ], string='Bộ Phận', required=True, track_visibility="always")
    # employee_status = fields.Selection([
    #     ('part time', 'Part Time'),
    #     ('full time', 'Full Time'),
    # ], string='Làm Việc', required=True, track_visibility="always")
    # employee_salary = fields.Float(string='Lương Cơ Bản', required=True, track_visibility="always")
    # notes = fields.Text(string="Ghi Chú")

    # create sequence for advance salary record
    @api.model
    def create(self, vals):
        if vals.get('advance_salary_record_seq', _('New')) == _('New'):
            vals['advance_salary_record_seq'] = self.env['ir.sequence'].next_by_code('salesman.advance.salary.sequence') \
                                                or _('New')
        result = super(HRAdvanceSalary, self).create(vals)
        return result


class EmployeeAdvanceSalaryRecord(models.Model):
    _name = 'salesman.advance.salary.record'
    _description = 'Advance Salary Record'

    employee_id = fields.Char(string="Mã NV", related="item_id.employee_seq")
    item_id = fields.Many2one('salesman.employee', string='Tên NV')
    employee_dept = fields.Char(string="Bộ Phận", related="item_id.employee_group_store")
    basic_salary = fields.Float(string="Lương Cơ Bản", related="item_id.employee_salary")
    advance_salary = fields.Float(string="Tạm Ứng")
    advance_month = fields.Date(string="Tháng")
    advance_notes = fields.Text(string='Ghi Chú')
    doc_id = fields.Many2one('salesman.advance.salary', string="Mã Phiếu")

    # @api.depends('item_price', 'item_quantity')
    # def _get_total(self):
    #     for val in self:
    #         if val.doc_id:
    #             val.item_total = val.item_price * val.item_quantity

    # @api.model
    # def create(self, vals):
    #     result = super(EmployeeSalaryRecord, self).create(vals)
    #     storage_id = vals['item_id']
    #     if storage_id:
    #         storage = self.env['inventory.storage'].search([('id', '=', storage_id)])
    #         storage.quantity = storage.quantity - vals['item_quantity']
    #         print('ketqua', storage.quantity)
    #         if storage.quantity < vals['item_quantity']:
    #             p_name = storage.product_name
    #             raise ValidationError(_('Không Đủ %s Để Xuất Kho') % (p_name))
    #     return result


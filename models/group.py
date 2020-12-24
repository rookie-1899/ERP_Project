# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from datetime import datetime


class GroupProduct(models.Model):
    _name = 'inventory.group'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Grouping'
    _rec_name = 'group_name'

    group_name = fields.Char(string="Tên Nhóm NVL", required=True)
    created_date = fields.Date(string="Ngày Tạo", required="True",
                               default=lambda self: fields.Date.today(), readonly=True)
    group_seq = fields.Char(string='Mã Nhóm NVL', required=True, copy=False, readonly=True,
                            index=True, default=lambda self: _('New'))
    notes = fields.Text(string="Ghi Chú")

    # create sequence for group product
    @api.model
    def create(self, vals):
        if vals.get('group_seq', _('New')) == _('New'):
            vals['group_seq'] = self.env['ir.sequence'].next_by_code('inventory.group.sequence') or _('New')
        result = super(GroupProduct, self).create(vals)
        return result

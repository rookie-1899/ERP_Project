# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MenuManagement(models.Model):
    _name = 'salesman.menu'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Menu of Restaurant'
    _rec_name = 'menu_name'
    _order = 'id desc'

    menu_seq = fields.Char(string='Mã Món', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    menu_name = fields.Char(string='Tên Món', required=True, track_visibility="always")
    menu_type = fields.Many2one("salesman.type", string='Loại Menu', required=True)
    menu_group = fields.Char(string='Nhóm Menu', related='menu_type.menu_group_name')
    menu_unit = fields.Char(string='Đơn Vị Món')
    menu_price = fields.Float(string='Đơn giá', required=True, track_visibility="always")
    menu_date = fields.Date(string="Ngày Tạo", required="True",
                            default=lambda self: fields.Date.today(), readonly=True)
    notes = fields.Text(string="Ghi Chú")

    # create sequence for NVL
    @api.model
    def create(self, vals):
        if vals.get('menu_seq', _('New')) == _('New'):
            vals['menu_seq'] = self.env['ir.sequence'].next_by_code('salesman.menu.sequence') or _('New')
        result = super(MenuManagement, self).create(vals)
        return result




# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MenuType(models.Model):
    _name = 'salesman.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Menu Group Record'
    _rec_name = 'type_name'
    _order = 'id desc'

    type_seq = fields.Char(string='Mã Loại Menu', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    type_name = fields.Char(string='Tên Loại Menu', required=True, track_visibility="always")
    notes = fields.Text(string="Ghi Chú")
    menu_group = fields.Selection([
        ('đồ ăn', 'Đồ Ăn'),
        ('đồ uống', 'Đồ Uống'),
    ], string='Nhóm Menu', required=True)

    menu_group_name = fields.Char(string='Tên Nhóm')

    # create sequence for NVL
    @api.model
    def create(self, vals):
        if vals.get('type_seq', _('New')) == _('New'):
            vals['type_seq'] = self.env['ir.sequence'].next_by_code('salesman.type.sequence') or _('New')
        result = super(MenuType, self).create(vals)
        return result

    # create sequence for NVL
    @api.constrains('menu_group')
    def check_group(self):
        for rec in self:
            if rec.menu_group == 'Chọn Nhóm Menu':
                raise ValidationError(_('Không Được Để Trống "%s"') % (rec.menu_group))

    # create sequence for NVL
    @api.onchange('menu_group')
    def set_menu_name(self):
        for rec in self:
            if rec.menu_group:
                if rec.menu_group == 'đồ ăn' or rec.menu_group == 'Đồ Ăn':
                    rec.menu_group_name = 'Đồ Ăn'
                    print('something', rec.menu_group_name)
                else:
                    rec.menu_group_name = 'Đồ Uống'
                    print('something', rec.menu_group_name)




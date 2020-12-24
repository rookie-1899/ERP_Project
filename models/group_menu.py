# -*- coding: utf-8 -*-

# from odoo import models, fields, api, _
# from odoo.exceptions import ValidationError
#
#
# class MenuGroup(models.Model):
#     _name = 'salesman.group'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = 'Menu Group Record'
#     _rec_name = 'group_name'
#     _order = 'id desc'
#
#     group_seq = fields.Char(string='Mã Nhóm Menu', required=True, copy=False, readonly=True,
#                             index=True, default=lambda self: _('New'))
#     group_name = fields.Char(string='Tên Nhóm Menu', required=True, track_visibility="always")
#     notes = fields.Text(string="Ghi Chú")
#
#     # create sequence for NVL
#     @api.model
#     def create(self, vals):
#         if vals.get('group_seq', _('New')) == _('New'):
#             vals['group_seq'] = self.env['ir.sequence'].next_by_code('salesman.group.sequence') or _('New')
#         result = super(MenuGroup, self).create(vals)
#         return result
#
#
#

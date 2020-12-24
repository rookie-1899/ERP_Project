# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StorageManagement(models.Model):
    _name = 'inventory.storage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Inventory Record'
    _rec_name = 'product_name'
    _order = 'id desc'

    @api.multi
    def open_storage_imports(self):
        return {
            'name': _('Imports'),
            # 'domain': ["seq_import", "=", self.id],
            'res_model': 'inventory.import',
            'views_id': False,
            'views': [(False, 'form')],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {},
        }

    product_name = fields.Char(string='Tên NVL', required=True, track_visibility="always")
    unit = fields.Char(string="Đơn Vị")
    image = fields.Binary(string='Image', default="")
    product_seq = fields.Char(string='Mã NVL', required=True, copy=False, readonly=True,
                              index=True, default=lambda self: _('New'))
    price = fields.Float(string="Giá trung bình")
    quantity = fields.Float(string='Số lượng/Khối lượng', required=True, store=True, track_visibility="always")
    group = fields.Many2one('inventory.group', string="Nhóm NVL", required=True)
    notes = fields.Text(string="Ghi Chú", track_visibility="always")
    total = fields.Float(string='Thành Tiền Nhập Kho', required=True, compute="_get_total", store=True)
    min_qua = fields.Float(string='Tồn Tối Thiểu', required=True, default="0")
    # storage_change = fields.Float(string='Thành Tiền Xuất Kho', required=False, store=True, track_visibility="always")

    @api.depends('price', 'quantity')
    def _get_total(self):
        for value in self:
            value.total = value.price * value.quantity
        # self.total = self.price * self.quantity

    # @api.model
    # def _update_storage_upon_import(self):
    #     for val in self:
    #         val.count = self.env['inventory.export.line'].search([('id', '=', self.id)])
    #         val.storage_change = val.count.item_total
    #     return val.storage_change

    # create sequence for NVL
    @api.model
    def create(self, vals):
        if vals.get('product_seq', _('New')) == _('New'):
            vals['product_seq'] = self.env['ir.sequence'].next_by_code('inventory.storage.sequence') or _('New')
        result = super(StorageManagement, self).create(vals)
        return result

    @api.constrains('quantity', 'price')
    def check_quantity(self):
        for value in self:
            if value.quantity < 0:
                raise ValidationError(_('Trong Kho Không Đủ "%s" Để Xuất') % (self.product_name))

    def check_price(self):
        for value in self:
            if value.price < 0:
                raise ValidationError(_("Giá trung bình không thể âm"))


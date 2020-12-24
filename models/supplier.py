# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SupplierManagement(models.Model):
    _name = 'inventory.supplier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Inventory Supplier Record'
    _rec_name = 'supplier_name'
    _order = 'id desc'

    supplier_seq = fields.Char(string='Mã NCC', required=True, copy=False, readonly=True,
                               index=True, default=lambda self: _('New'))
    supplier_name = fields.Char(string='Tên NCC', required=True, track_visibility="always")
    address = fields.Text(string="Địa Chỉ", track_visibility="always")
    phone_num = fields.Char(string="Số Điện Thoại", required=False)
    notes = fields.Text(string="Ghi Chú")

    # create sequence for NVL
    @api.model
    def create(self, vals):
        if vals.get('supplier_seq', _('New')) == _('New'):
            vals['supplier_seq'] = self.env['ir.sequence'].next_by_code('inventory.supplier.sequence') or _('New')
        result = super(SupplierManagement, self).create(vals)
        return result




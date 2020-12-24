# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from datetime import datetime


class WarehouseImport(models.Model):
    _name = 'inventory.import'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Storage Updated'
    _rec_name = 'seq_import'
    _order = 'id desc'

    date_import = fields.Date(string="Ngày Nhập Kho", required="True",
                              default=lambda self: fields.Date.today(), readonly=True)
    seq_import = fields.Char(string='Mã Phiếu Nhập Kho', required=True, copy=False, readonly=True,
                             index=True, default=lambda self: _('New'))
    product_line = fields.One2many(comodel_name="inventory.import.line",
                                   inverse_name="doc_id", string="Thêm NVL", required=True, )
    notes = fields.Text(string="Ghi Chú")

    # create sequence for group product
    @api.model
    def create(self, vals):
        if vals.get('seq_import', _('New')) == _('New'):
            vals['seq_import'] = self.env['ir.sequence'].next_by_code('inventory.import.sequence') or _('New')
        result = super(WarehouseImport, self).create(vals)
        return result


class WarehouseImportLine(models.Model):
    _name = 'inventory.import.line'
    _description = 'Product Line'

    item_id = fields.Many2one('inventory.storage', string='NVL')
    item_supplier_id = fields.Many2one('inventory.supplier', string="NCC")
    item_quantity = fields.Float(string="Số Lượng Nhập")
    item_unit = fields.Char(string="Đơn vị", related='item_id.unit')
    current_quantity = fields.Float(string="Lượng Tồn Kho", related='item_id.quantity', compute="_get_residual")
    doc_id = fields.Many2one('inventory.import', string="Mã Phiếu")
    item_price = fields.Float(string="Đơn Giá")
    item_total = fields.Float(string='Thành Tiền', compute="_get_total", store=True)

    @api.depends('item_price', 'item_quantity')
    def _get_total(self):
        for val in self:
            if val.doc_id:
                val.item_total = val.item_price * val.item_quantity

    @api.model
    def create(self, vals):
        result = super(WarehouseImportLine, self).create(vals)
        # for item in result:
        #     item.new_line = vals['item_id']
        #     if item.new_line:
        #         storage = self.env['inventory.storage'].search([('id', '=', item.new_line)])
        #         storage.price = ((vals['item_price'] * vals['item_quantity']) + (storage.quantity * storage.price)) / (storage.quantity + vals['item_quantity'])
        #         print('ketqua', storage.price)
        a = vals['item_id']
        b = self.env['inventory.storage'].search([('id', '=', a)])
        print("So luong", vals['item_quantity'])
        if b:
            b.quantity += vals['item_quantity']
            b.price = ((vals['item_price'] * vals['item_quantity']) + (b.quantity * b.price)) / (b.quantity + vals['item_quantity'])
        print("Ket qua", a)
        return result

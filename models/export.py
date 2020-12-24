# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from datetime import datetime


class WarehouseExport(models.Model):
    _name = 'inventory.export'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Storage Updated'
    _rec_name = 'seq_export'
    _order = 'id desc'

    date_export = fields.Date(string="Ngày Xuất Kho", required="True",
                              default=lambda self: fields.Date.today(), readonly=True)
    seq_export = fields.Char(string='Mã Phiếu Xuất Kho', required=True, copy=False, readonly=True,
                             index=True, default=lambda self: _('New'))
    total_export = fields.Float(string="Tổng Tiền")
    # product_export = fields.Many2many("inventory.storage", string="Table")
    product_line = fields.One2many(comodel_name="inventory.export.line", inverse_name="doc_id", string="Thêm NVL")
    notes = fields.Text(string="Ghi Chú")

    # create sequence for group product
    @api.model
    def create(self, vals):
        if vals.get('seq_export', _('New')) == _('New'):
            vals['seq_export'] = self.env['ir.sequence'].next_by_code('inventory.export.sequence') or _('New')
        result = super(WarehouseExport, self).create(vals)
        return result


class WarehouseExportLine(models.Model):
    _name = 'inventory.export.line'
    _description = 'Product Line'

    item_id = fields.Many2one('inventory.storage', string='NVL')
    item_quantity = fields.Float(string="Số Lượng/Khối Lượng")
    current_quantity = fields.Float(string="Số Lượng Tồn", related="item_id.quantity")
    item_unit = fields.Char(string="Đơn vị", related="item_id.unit")
    doc_id = fields.Many2one('inventory.export', string="Mã Phiếu")
    item_price = fields.Float(string="Đơn Giá", related="item_id.price")
    item_total = fields.Float(string='Thành Tiền', compute="_get_total")

    @api.depends('item_price', 'item_quantity')
    def _get_total(self):
        for val in self:
            if val.doc_id:
                val.item_total = val.item_price * val.item_quantity

    @api.model
    def create(self, vals):
        result = super(WarehouseExportLine, self).create(vals)
        storage_id = vals['item_id']
        if storage_id:
            storage = self.env['inventory.storage'].search([('id', '=', storage_id)])
            storage.quantity = storage.quantity - vals['item_quantity']
            print('ketqua', storage.quantity)
            if storage.quantity < vals['item_quantity']:
                p_name = storage.product_name
                raise ValidationError(_('Không Đủ %s Để Xuất Kho') % (p_name))
        return result

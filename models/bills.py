# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from datetime import datetime


class ReceiptManagement(models.Model):
    _name = 'salesman.receipt'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bill for Customers'
    _rec_name = 'seq_receipt'
    _order = 'id desc'

    seq_receipt = fields.Char(string='Mã Hóa Đơn Bán', required=True, copy=False, readonly=True,
                              index=True, default=lambda self: _('New'))
    date_receipt = fields.Date(string="Ngày Xuất", required="True",
                               default=lambda self: fields.Date.today(), readonly=True)
    total_receipt = fields.Float(string="Tổng Hóa Đơn")
    # product_export = fields.Many2many("inventory.storage", string="Table")
    menu_order = fields.One2many(comodel_name="salesman.receipt.line", inverse_name="doc_id", string="Order")
    notes = fields.Text(string="Ghi Chú")
    customer_name = fields.Char(string='Tên Khách Hàng', required=False)

    # create sequence for group product
    @api.model
    def create(self, vals):
        if vals.get('seq_receipt', _('New')) == _('New'):
            vals['seq_receipt'] = self.env['ir.sequence'].next_by_code('salesman.receipt.sequence') or _('New')
        result = super(ReceiptManagement, self).create(vals)
        return result


class ReceiptOrderLine(models.Model):
    _name = 'salesman.receipt.line'
    _description = 'Order Line'

    doc_id = fields.Many2one('salesman.receipt', string="Mã Phiếu")
    item_id = fields.Many2one('salesman.menu', string='Tên Order')
    item_unit = fields.Char(string="Đơn vị", related="item_id.menu_unit")
    item_quantity = fields.Float(string="Số Lượng/Khối Lượng")
    item_price = fields.Float(string="Đơn Giá", related="item_id.menu_price")
    item_total = fields.Float(string='Thành Tiền', compute="_get_total")

    @api.depends('item_price', 'item_quantity')
    def _get_total(self):
        for val in self:
            if val.doc_id:
                val.item_total = val.item_price * val.item_quantity

    # @api.model
    # def create(self, vals):
    #     result = super(ReceiptOrderLine, self).create(vals)
    #
    #     return result

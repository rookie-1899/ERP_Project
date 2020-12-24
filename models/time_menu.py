# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TimeMenu(models.Model):
    _name = 'salesman.time.menu'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Seasonal Menus'
    _rec_name = 'time_menu_name'
    _order = 'id desc'

    time_menu_seq = fields.Char(string='Mã Món', required=True, copy=False, readonly=True,
                                index=True, default=lambda self: _('New'))
    time_menu_name = fields.Char(string='Tên Thực Đơn Mới', required=True, track_visibility="always")
    start_time = fields.Date(string='Ngày Áp Dụng')
    end_time = fields.Date(string='Ngày Kết Thúc')
    menu_items = fields.One2many(comodel_name="salesman.menu.items",
                                 inverse_name="doc_id", string="Thêm Mặt Hàng", required=True, )
    notes = fields.Text(string='Ghi Chú')
    # notes = fields.Text(string="Ghi Chú")

    # create sequence for NVL
    @api.model
    def create(self, vals):
        if vals.get('time_menu_seq', _('New')) == _('New'):
            vals['time_menu_seq'] = self.env['ir.sequence'].next_by_code('salesman.time.menu.sequence') or _('New')
        result = super(TimeMenu, self).create(vals)
        return result


class MenuItems(models.Model):
    _name = 'salesman.menu.items'
    _description = 'Menu Items'

    item_id = fields.Many2one('salesman.menu', string='Mặt Hàng')
    item_menu_group = fields.Char(string='Nhóm Mặt Hàng', related='item_id.menu_group')
    current_item_price = fields.Float(string="Giá Mặt Hàng Hiện Tại", related='item_id.menu_price')
    item_price = fields.Float(string="Giá Mới")
    doc_id = fields.Many2one('salesman.time.menu', string="Mã Phiếu")

    # @api.depends('item_price', 'item_quantity')
    # def _get_total(self):
    #     for val in self:
    #         if val.doc_id:
    #             val.item_total = val.item_price * val.item_quantity

    @api.model
    def create(self, vals):
        result = super(MenuItems, self).create(vals)
        # for item in result:
        #     item.new_line = vals['item_id']
        #     if item.new_line:
        #         storage = self.env['inventory.storage'].search([('id', '=', item.new_line)])
        #         storage.price = ((vals['item_price'] * vals['item_quantity']) + (storage.quantity * storage.price)) / (storage.quantity + vals['item_quantity'])
        #         print('ketqua', storage.price)
        a = vals['item_id']
        b = self.env['salesman.menu'].search([('id', '=', a)])
        if b:
            b.menu_price = 0
            b.menu_price = vals['item_price']
        print("Ket qua", b)
        return result

    # @api.model
    # def match_product(self, vals):
    #     a = vals['item_id']
    #     b = self.env['salesman.menu'].search([('id', '=', a)])
    #     if b.menu_group == vals.item_menu_group:
    #         return vals.item_id
    #     else:
    #         raise ValidationError(_('Mặt Hàng Không Đúng Định Dạng "%s"') % (self.item_menu_group))

# -*- coding: utf-8 -*-
{
    'name': "inventory_management",

    'summary': """Xuất nhập tồn kho""",

    'description': """
        Quản lý nguyên vật liệu nhập xuất tồn kho
    """,

    'author': "Banking Academy",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Phần mềm quản lý',
    'version': '0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/storage.xml',
        'views/group.xml',
        'views/import.xml',
        'views/export.xml',
        'views/supplier.xml',
        'views/menu.xml',
        'views/bills.xml',
        'views/type_menu.xml',
        'views/employees.xml',
        'views/salary.xml',
        'views/advance_salary.xml',
        'views/time_menu.xml',
        'data/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
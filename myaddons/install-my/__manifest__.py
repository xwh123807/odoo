# -*- coding: utf-8 -*-
{
    'name': "install-my",

    'summary': """
        定制安装项目
    """,

    'description': """
        定制安装项目
    """,

    'author': "xwh",
    'website': "http://www.xwh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'xwh',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'crm', 'project', 'account', 'sale_management', 'note', 'purchase',
                'hr', 'hr_expense', 'board', 'stock', 'mrp', 'hr_attendance', 'hr_recruitment',
                'hr_holidays', 'survey', 'lunch', 'maintenance', 'fleet', 'repair'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

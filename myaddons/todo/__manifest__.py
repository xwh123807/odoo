# -*- coding: utf-8 -*-
{
    'name': "todo",

    'summary': """
        工作计划管理
    """,

    'description': """
        工作计划管理：安排你的工作计划
    """,

    'author': "xwh",
    'website': "http://www.xwh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'xwh',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/todo_record_rules.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
{
    'name': "Memoree",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
            Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/memoree_menu.xml',
        'views/vocab_import.xml',
        'views/vocab_test.xml',
        'views/vocab_test_daily.xml',
        'views/vocab_topic.xml',
    ],
    'demo': [
    ],
}


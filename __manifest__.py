# -*- coding: utf-8 -*-
{
    'name': "charging",

    'summary': """
        odoo 12 module for manages electric charging stations charges 
        and for calculating the final price for the customer of their
        charging sessions""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report_xlsx'],

    # always loaded
    'data': [
        'security/charging_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/transactions_view.xml',
        'views/supplier_prices_view.xml',
        'wizard/excel_wizard.xml',
        'report/charging_excel_report_views.xml',
        'report/charging_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
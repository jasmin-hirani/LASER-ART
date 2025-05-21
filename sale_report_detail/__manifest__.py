{
    'name': 'GST Bill Detailed Report',
    'version': '17.0.1.0',
    'summary': 'Custom report to display sale order GST details within a date range',
    'description': """
    This module generates a detailed report of sale orders GST Details within a specified date range.
    """,
    'category': 'Sales',
    'author': 'Tatvamasi Labs',
    'depends': ['base','sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_report_view.xml',
        'report/sale_order_report_template.xml',
    ],
    'license':"LGPL-3",
    'installable': True,
    'application': False,
    'auto_install': False,
}
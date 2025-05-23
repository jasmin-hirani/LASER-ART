{
    'name': 'GST Bill Detailed Report',
    'version': '18.0.0.0.0',
    'summary': 'Custom report to display invoice GST details within a date range',
    'description': """
This module generates a detailed report of invoice GST details within a specified date range.
""",
    'category': 'Accounting',
    'author': 'Tatvamasi Labs',
    'website': "https://tatvamasilabs.com/",
    'depends': ['base', 'account', 'l10n_in'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_paper_format.xml',
        'report/gst_report_template.xml',
        'views/gst_report_wizard_view.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}

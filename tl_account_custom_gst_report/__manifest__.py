# -*- coding: utf-8 -*-
{
    'name': "Account Custom GSTR-3 Report",
    'summary': """
        Account Custom GSTR-3 Report And Other Fields
    """,
    'version': '18.0.0.0',
    'description': """
        Account Custom GSTR-3 Report And Other Fields
    """,
    'author': "Tatvamasi Labs",
    'website': "https://www.tatvamasilabs.com",
    'category': 'Accounting',
    'depends': ['account', 'l10n_in', 'account_edi', 'l10n_in_edi_ewaybill', 'l10n_in_withholding'],
    'data': [
        'views/account_move_view.xml',
        'views/report_gstr3b_custom.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}

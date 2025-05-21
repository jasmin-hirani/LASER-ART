from odoo import models, fields, api
from datetime import date

class SaleOrderReport(models.TransientModel):
    _name = 'sale.order.report.wizard'
    _description = 'Sale Order Report'

    date_from = fields.Date(
        string='Date From',
        required=True,
        default=date.today().replace(day=1)
    )

    date_to = fields.Date(
        string='Date To',
        required=True,
        default=date.today()
    )

    def action_print_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
            },
        }
        return self.env.ref('sale_report_detail.action_sale_order_detail_report').report_action(self, data=data)
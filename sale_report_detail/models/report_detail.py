from odoo import models, fields, api

class ReportSaleOrderDetail(models.AbstractModel):
    _name = 'report.sale_report_detail.gst_bill_detail_report'
    _description = 'GST Bill Detail Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['sale.order.report.wizard'].browse(data.get('ids'))
        if not wizard:
            return {}

        date_from = data['form'].get('date_from')
        date_to = data['form'].get('date_to')

        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', date_from),
            ('date_order', '<=', date_to),
        ])

        return {
            'doc_ids': sale_orders.ids,
            'doc_model': 'sale.order',
            'docs': sale_orders,
            'date_from': date_from,
            'date_to': date_to,
        }

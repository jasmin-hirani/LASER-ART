from odoo import models, fields, api

class ReportGSTDetail(models.AbstractModel):
    _name = 'report.tl_gst_detail_report.gst_bill_detail_report'
    _description = 'GST Bill Detail Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['gst.report.wizard'].browse(data.get('ids'))
        if not wizard:
            return {}

        date_from = data['form'].get('date_from')
        date_to = data['form'].get('date_to')

        invoices = self.env['account.move'].search([
            # ('move_type', '=', 'out_invoice'),
            # ('state', '=', 'posted'),
            ('invoice_date', '>=', date_from),
            ('invoice_date', '<=', date_to),
        ], order='invoice_date asc')

        return {
            'doc_ids': invoices.ids,
            'doc_model': 'account.move',
            'docs': invoices,
            'date_from': date_from,
            'date_to': date_to,
        }

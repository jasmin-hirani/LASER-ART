# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    cgst_amount = fields.Monetary(
        string='CGST Amount',
        compute='_compute_gst_amounts',
        store=True,
        currency_field='company_currency_id',
    )
    sgst_amount = fields.Monetary(
        string='SGST Amount',
        compute='_compute_gst_amounts',
        store=True,
        currency_field='company_currency_id',
    )
    igst_amount = fields.Monetary(
        string='IGST Amount',
        compute='_compute_gst_amounts',
        store=True,
        currency_field='company_currency_id',
    )
    partner_gst_number = fields.Char('GST Number', related='partner_id.vat', store=True)
    e_invoice_status = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'E-Invoice Status', compute='_compute_e_invoice_status')
    e_way_bill_status = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'E-Way Bill Status', compute='_compute_e_way_bill_status')
    tds_amount = fields.Monetary('TDS Amount', compute='_compute_gst_amounts', currency_field='company_currency_id')

    @api.depends('edi_document_ids')
    def _compute_e_invoice_status(self):
        for invoice in self:
            status = bool(invoice.edi_document_ids.filtered(
                lambda i: i.edi_format_id.code == "in_einvoice_1_03" and i.state == "sent"))
            if status == True:
                invoice.e_invoice_status = 'yes'
            else:
                invoice.e_invoice_status = 'no'

    @api.depends('edi_document_ids')
    def _compute_e_way_bill_status(self):
        for invoice in self:
            status = bool(invoice.edi_document_ids.filtered(
                lambda i: i.edi_format_id.code == "in_ewaybill_1_03" and i.state == "sent"))
            if status == True:
                invoice.e_way_bill_status = 'yes'
            else:
                invoice.e_way_bill_status = 'no'

    @api.depends('tax_totals')
    def _compute_gst_amounts(self):
        for move in self:
            cgst = sgst = igst = tds = 0.0

            # Check if 'subtotals' is available in tax_totals
            if move.tax_totals and 'subtotals' in move.tax_totals:
                for subtotal in move.tax_totals['subtotals']:
                    # Iterate through tax groups in the current subtotal
                    for group in subtotal['tax_groups']:
                        group_name = group.get('group_name', '').lower()
                        tax_amount = group.get('tax_amount', 0.0)

                        if group_name == 'sgst':
                            sgst += tax_amount
                        elif group_name == 'cgst':
                            cgst += tax_amount
                        elif group_name == 'igst':
                            igst += tax_amount
                        elif group_name == 'tds':
                            tds += tax_amount

            # Update the fields
            move.cgst_amount = cgst
            move.sgst_amount = sgst
            move.igst_amount = igst
            move.tds_amount = tds


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pan_number = fields.Char('PAN', related='partner_id.l10n_in_pan', store=True)
    gst_number = fields.Char('GST Number', related='partner_id.vat', store=True)
    amount_untaxed = fields.Monetary('Untaxed Amount', related='move_id.amount_untaxed', store=True, currency_field='company_currency_id')
    amount_with_gst = fields.Monetary('Tax Amount', compute="_compute_amount_with_gst")
    tds_line_amount = fields.Monetary('TDS Line Amount', compute="_compute_tds_line_amount")
    amount_total = fields.Monetary(related="move_id.amount_total", string="Total Amount")
    
    @api.depends('tax_line_id', 'tax_ids', 'price_subtotal', 'price_total', 'tax_base_amount', 'move_id.tax_totals')
    def _compute_amount_with_gst(self):
        for line in self:
            total_untaxed = 0
            for move in line.move_id.invoice_line_ids:
                total_untaxed += move.price_subtotal
            line.amount_with_gst = total_untaxed + line.move_id.cgst_amount + line.move_id.sgst_amount + line.move_id.igst_amount
            
    @api.depends('tax_line_id', 'tax_ids', 'price_subtotal', 'price_total', 'tax_base_amount', 'move_id.tax_totals')
    def _compute_tds_line_amount(self):
        for line in self:
            tds_line_amount = 0
            for move in line.move_id.invoice_line_ids:
                if line.tax_line_id.id in  move.tax_ids.ids:
                    tds_line_amount += move.price_subtotal
            line.tds_line_amount = tds_line_amount
                

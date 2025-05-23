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

    total_discount_amount = fields.Monetary(
        string="Total Discount",
        compute="_compute_total_discount",
        store=True,
        currency_field='company_currency_id'
    )

    @api.depends('invoice_line_ids.discount_amount')
    def _compute_total_discount(self):
        for move in self:
            move.total_discount_amount = sum(move.invoice_line_ids.mapped('discount_amount'))

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

            # Update the fields
            move.cgst_amount = cgst
            move.sgst_amount = sgst
            move.igst_amount = igst


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    cgst_rate = fields.Float(string="CGST (%)", compute="_compute_gst_data", store=True)
    sgst_rate = fields.Float(string="SGST (%)", compute="_compute_gst_data", store=True)
    igst_rate = fields.Float(string="IGST (%)", compute="_compute_gst_data", store=True)

    cgst_amount = fields.Monetary(string="CGST Amount",
                                  compute="_compute_gst_data", store=True,
                                  currency_field='company_currency_id')
    sgst_amount = fields.Monetary(string="SGST Amount",
                                  compute="_compute_gst_data", store=True,
                                  currency_field='company_currency_id')
    igst_amount = fields.Monetary(string="IGST Amount",
                                  compute="_compute_gst_data", store=True,
                                  currency_field='company_currency_id')

    amount_with_tax = fields.Monetary(string="Total with Tax",
                                      compute="_compute_gst_data", store=True,
                                      currency_field='company_currency_id')
    discount_amount = fields.Monetary(
        string="Discount Amount",
        compute="_compute_discount_amount",
        store=True,
        currency_field='company_currency_id'
    )

    @api.depends('price_unit', 'quantity', 'discount')
    def _compute_discount_amount(self):
        for line in self:
            line.discount_amount = (line.price_unit * line.quantity) * (line.discount / 100.0)

    @api.depends('tax_ids', 'price_subtotal')
    def _compute_gst_data(self):
        for line in self:
            cgst = sgst = igst = 0.0
            cgst_amt = sgst_amt = igst_amt = 0.0

            all_taxes = line.tax_ids.mapped('children_tax_ids') or line.tax_ids

            for tax in all_taxes:
                group = (tax.tax_group_id.name or '').strip().lower()
                rate = tax.amount
                amount = line.price_subtotal * rate / 100.0

                if group == 'cgst':
                    cgst += rate
                    cgst_amt += amount
                elif group == 'sgst':
                    sgst += rate
                    sgst_amt += amount
                elif group == 'igst':
                    igst += rate
                    igst_amt += amount

            line.cgst_rate = cgst
            line.sgst_rate = sgst
            line.igst_rate = igst
            line.cgst_amount = cgst_amt
            line.sgst_amount = sgst_amt
            line.igst_amount = igst_amt

            line.amount_with_tax = line.price_subtotal + cgst_amt + sgst_amt + igst_amt

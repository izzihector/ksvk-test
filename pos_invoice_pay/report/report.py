# Copyright 2018 Artyom Losev
# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, models


class ReportSaleDetails(models.AbstractModel):
    _inherit = "report.point_of_sale.report_saledetails"

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, configs=False, session_ids=False):
        config = self.env["pos.config"].search([
            ("currency_id", "in", configs)
        ])
        res = super(ReportSaleDetails, self).get_sale_details(
            date_start, date_stop, configs, session_ids
        )
        payments = self.env["account.payment"].search(
            [
                ("datetime", ">=", date_start),
                ("datetime", "<=", date_stop),
                ("pos_session_id", "in", config.session_ids.ids),
            ]
        )
        res["invoices"] = []
        unique = []
        res["total_invoices"] = res["total_invoices_cash"] = 0.0
        for p in payments:
            if p.invoice_ids.id not in unique:
                invoice = p.invoice_ids
                cashier = p.cashier
                data = {
                    "invoice_no": invoice.name,
                    "so_origin": invoice.invoice_origin,
                    "customer": invoice.partner_id.name,
                    "payment_method": p.payment_method_id.name,
                    "cashier": cashier.name or cashier.partner_id.name,
                    "amount_total": invoice.amount_total,
                    "amount": p.amount,
                }
                res["invoices"].append(data)
                res["total_invoices"] += p.amount
                if p.journal_id.type == "cash":
                    res["total_invoices_cash"] += p.amount
        return res

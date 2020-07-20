# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import xlsxwriter
from odoo import models


class ChargingXlsx(models.AbstractModel):
    _name = 'report.charging_excel_report.charging_report_xls.xslx'
    _inherit = 'report.report_xlsx.abstract'

    def get_lines(self, obj):
        lines = []
        charging = self.env['supplier.prices'].search([])
        for value in charging:
            vals = {
                'fee_price': value.fee_price,
                'time_price': value.time_price,
                'kwh_price': value.total_kwh_price,
                'total_price': value.total_price,
                'session_id': value.identifier,
                'supplier_price_id': value.evse_id,
                }
            lines.append(vals)
        return lines

    def generate_xlsx_report(self, workbook, data, wizard_obj):
        for obj in wizard_obj:
            lines = self.get_lines(obj)
            worksheet = workbook.add_worksheet('Report')
            gold = workbook.add_format({'bold': True, 'align': 'left'})
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})
            left = workbook.add_format({'font_size': 12, 'align': 'left'})
            right = workbook.add_format({'font_size': 12, 'align': 'right'})
            worksheet.set_column(0, 0, 20)
            worksheet.set_column(1, 2, 20)
            worksheet.set_column(3, 3, 20)
            worksheet.set_column(4, 4, 20)
            worksheet.set_column(5, 5, 20)
            worksheet.set_column(6, 6, 20)
            worksheet.set_column(7, 7, 20)
            worksheet.write('D2', 'Charging Cost', bold)
            worksheet.write('A5', 'Fee Price', bold)
            worksheet.write('B5', 'Time Price', bold)
            worksheet.write('C5', 'KWH Price', bold)
            worksheet.write('D5', 'Total Price', bold)
            worksheet.write('E5', 'Session Id', bold)
            worksheet.write('F5', 'Supplier Price Id', bold)
            row = 5
            col = 0
            for res in lines:
                worksheet.write(row, col, res['fee_price'], text)
                worksheet.write(row, col + 1, res['time_price'], left)
                worksheet.write(row, col + 2, res['kwh_price'], right)
                worksheet.write(row, col + 5, res['total_price'], text)
                worksheet.write(row, col + 7, res['session_id'], text)
                worksheet.write(row, col + 9, res['supplier_price_id'], text)
                row = row + 1



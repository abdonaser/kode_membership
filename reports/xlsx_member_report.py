from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval


class XlsxPropertyReport(http.Controller):

    @http.route('/member/excel/report/<string:member_ids>', type='http', auth='user')
    def download_property_excel_report(self, member_ids):
        print("="*20)
        print('string:member_ids ' , member_ids)
        member_ids = request.env['kode.member'].browse(literal_eval(member_ids))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Members')

        # Formats
        # Header format: bold, centered, with a solid background color and border
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#4F81BD',   # A more modern blue header
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })

        # ========== Styles ==========
        header_format = workbook.add_format({
            'bold': True,
            'font_color': 'white',
            'bg_color': '#2F75B5',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': 12
        })

        string_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': 11
        })
        alt_row_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#F2F2F2',
            'text_wrap': True,
            'font_size': 11
        })
        date_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd',
            'font_size': 11
        })
        # Format monetary value with currency
        currency_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 11
        })


        # Freeze header row
        worksheet.freeze_panes(1, 0)



        # Header row
        headers = ['English Full Name', 'Arabic Full Name', 'First Name', 'Last Name',
                   'Status', 'Last Renewal Date', 'Total Last Renewal Order']

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
            worksheet.set_column(col_num, col_num, 20)

        row_num = 1
        for member in member_ids:
            row_format = alt_row_format if row_num % 2 == 0 else string_format
            worksheet.set_row(row_num, 40)

            currency_symbol = member.currency_id.symbol if member.currency_id else ''
            amount_str = f"{currency_symbol} {member.total_last_renewal_data:,.2f}" if member.total_last_renewal_data else ''

            worksheet.write(row_num, 0, member.name or '', row_format)
            worksheet.write(row_num, 1, member.arabic_name or '', row_format)
            worksheet.write(row_num, 2, member.first_name or '', row_format)
            worksheet.write(row_num, 3, member.last_name or '', row_format)
            worksheet.write(row_num, 4, member.status or '', row_format)
            worksheet.write(row_num, 5, member.last_renewal_date or '', date_format if member.last_renewal_date else row_format)
            worksheet.write(row_num, 6, amount_str, row_format)

            row_num += 1

        workbook.close()
        output.seek(0)
        xlsx_data = output.getvalue()
        output.close()

        return request.make_response(
            xlsx_data,
            headers =[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename*=UTF-8\'\'member_report.xlsx')
            ]
            )
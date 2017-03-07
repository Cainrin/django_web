# -*- coding: utf-8 -*-
import xlwt, datetime
from django.db import connection
from campaigns.foundation.const import FoundationConst


def write_table_in_excel(table, sheet_name):
    excel = xlwt.Workbook(encoding=FoundationConst.ENCODE_UTF8)
    sheet = excel.add_sheet(sheet_name)
    style = xlwt.easyxf(FoundationConst.EXPORT_EXCEL_STYLE)
    for row_index, row_list in enumerate(table):
        for col_index, val in enumerate(row_list):
            sheet.write(row_index, col_index, val, style)
            col_width_length = 200 + len(val) * 256
            now_length = sheet.col(col_index).width
            if col_width_length > now_length:
                sheet.col(col_index).width = col_width_length
    return excel


def export_queryset_to_excel(queryset, fields=None, exclude=None, header=True):
    opts = queryset.model._meta
    column_name_list = [field.name for field in opts.fields]
    if fields and isinstance(fields, list):
        column_name_list = fields
    elif exclude and isinstance(exclude, list):
        for field in exclude:
            column_name_list.remove(field)
    # 表名称
    sheet_name = opts.verbose_name.encode(FoundationConst.ENCODE_UTF8)
    # 列名称 与 列对像
    column_caption_list = list()
    column_obj_list = list()
    for field in opts.fields:
        if field.name in column_name_list:
            column_caption_list.append(field.verbose_name.encode(FoundationConst.ENCODE_UTF8))
            column_obj_list.append(field)
    # 数据详情展示
    table = list()
    table.append(column_caption_list)
    for obj in queryset:
        row_list = list()
        for column_obj in column_obj_list:
            val = obj._get_FIELD_display(column_obj)
            if isinstance(val, unicode):
                val = val.encode(FoundationConst.ENCODE_UTF8)
            elif isinstance(val, datetime.datetime):
                val = val.strftime("%Y年%m月%d日")
            elif isinstance(val, bool):
                val = FoundationConst.EXPORT_BOOL_TRUE if val else FoundationConst.EXPORT_BOOL_FALSE
            elif val is None:
                val = ""
            else:
                val = str(val)
            row_list.append(val)
        table.append(row_list)
    return write_table_in_excel(table, sheet_name)


def export_sql_to_excel(sql, sheet_name, column_caption_list=None):
    cursor = connection.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    table = list()
    table.extend(data_list)
    if column_caption_list is not None and isinstance(column_caption_list, list):
        table.insert(0, column_caption_list)
    return write_table_in_excel(table, sheet_name)

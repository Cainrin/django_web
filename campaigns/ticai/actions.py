# -*- coding: utf-8 -*-
from django.http import HttpResponse
from .const import FoundationConst
from .applet import export


def action_export_excel(description=FoundationConst.ACTION_EXPORT_EXCEL, fields=None, exclude=None, header=True):
    def export_excel(model_admin, request, queryset):
        excel = export.export_queryset_to_excel(queryset, fields=fields, exclude=exclude, header=header)
        opts = model_admin.model._meta
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename={0}.xls'.format(str(opts.verbose_name.encode('utf-8')).replace('.', '_'))
        excel.save(response)
        return response
    export_excel.short_description = description
    return export_excel


# 平台验证
def form_platform_validate(form):
    model = form.instance
    if model.platform == FoundationConst.PLATFORM_DESKTOP:
        if model.ip in [None, ""]:
            form.add_error(FoundationConst.PLATFORM_IP_NAME, Exception(FoundationConst.EXCEPTION_PLATFORM_IP))
        else:
            model.wxUser = None
    elif model.platform == FoundationConst.PLATFORM_WEIXIN:
        if model.wxUser in [None, ""]:
            form.add_error(FoundationConst.PLATFORM_WEIXIN_NAME, Exception(FoundationConst.EXCEPTION_PLATFORM_WEIXIN))
        else:
            model.ip = None

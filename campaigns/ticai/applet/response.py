# -*- coding: utf-8 -*-
import json
from django import http
from django.shortcuts import render_to_response
from campaigns.foundation.const import DisplayConst


def page_redirect(url):
    return http.HttpResponseRedirect(url)


def page_404(template_name):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def _page_response(status_code, template_name, data_dict, cookie_dict_list=None):
    response = render_to_response(template_name, data_dict)
    response.status_code = status_code
    if cookie_dict_list is not None:
        for cookie in cookie_dict_list:
            response.set_cookie(**cookie)
    return response


def page_success(template_name, data_dict=None, cookie_dict_list=None):
    return _page_response(200, template_name, data_dict, cookie_dict_list)


def page_400(template_name, data_dict=None, cookie_dict_list=None):
    return _page_response(400, template_name, data_dict, cookie_dict_list)


def page_403(template_name, data_dict=None, cookie_dict_list=None):
    return _page_response(403, template_name, data_dict, cookie_dict_list)


def page_500(template_name, data_dict=None, cookie_dict_list=None):
    return _page_response(500, template_name, data_dict, cookie_dict_list)


def page_501(template_name, data_dict=None, cookie_dict_list=None):
    return _page_response(501, template_name, data_dict, cookie_dict_list)


def _action_response(status_code, data_dict, cookie_dict_list=None):
    if data_dict is None:
        data_dict = dict()
    response = http.HttpResponse(json.dumps(data_dict), content_type=DisplayConst.CONTENT_TYPE_JSON)
    response.status_code = status_code
    if cookie_dict_list is not None:
        for cookie in cookie_dict_list:
            response.set_cookie(**cookie)
    return response


def action_success(data_dict=None, cookie_dict_list=None):
    return _action_response(200, data_dict, cookie_dict_list)


def action_400(data_dict=None, cookie_dict_list=None):
    return _action_response(400, data_dict, cookie_dict_list)


def action_forbidden(data_dict=None, cookie_dict_list=None):
    return _action_response(403, data_dict, cookie_dict_list)


def action_500(data_dict=None, cookie_dict_list=None):
    return _action_response(500, data_dict, cookie_dict_list)


def action_501(data_dict=None, cookie_dict_list=None):
    return _action_response(501, data_dict, cookie_dict_list)

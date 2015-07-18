#!/usr/bin/env python
# coding=utf-8
import os
import sys
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.http import HttpResponseNotFound
import json
def render_html(request, file_path, dict_value):
    template = loader.get_template(file_path)
    context = RequestContext(request, dict_value)
    return HttpResponse(template.render(context))


def make_json_response(_dict):
    json_str = json.dumps(_dict, ensure_ascii = False)
    return HttpResponse(json_str)

def make_404(string):
    return HttpResponseNotFound(string)

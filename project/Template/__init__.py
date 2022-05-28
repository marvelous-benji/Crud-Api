
from flask import Blueprint


template = Blueprint('template', __name__)

from .views import TemplateList, TemplateDetail

template_list = TemplateList.as_view("temp_list")
template_detail = TemplateDetail.as_view("temp_detail")


template.add_url_rule("", view_func=template_list, methods=["GET","POST"])

template.add_url_rule("/<id>", view_func=template_detail, methods=["GET","PUT","DELETE"])

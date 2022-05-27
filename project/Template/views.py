'''
This module contains all the endpoints
neccessary for the creation, display, update and deletion of templates
'''



from datetime import datetime
from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

from project import db, jwt
from . import template as temp
from ..models import Template, TemplateSchema, User




@temp.route("", methods=["POST"])
@jwt_required()
def add_template():
    data = request.get_json()
    serializer = TemplateSchema(exclude=('owner',))
    try:
        serialized_data = serializer.load(data)
    except ValidationError as err:
        return (
            jsonify(
                {
                    "status": "failed",
                    "msg": "Your inputs are invalid",
                    "error": err.messages,
                }
            ),
            400,
        )
    template_obj = Template(
        template_name=serialized_data["template_name"],
        subject=serialized_data["subject"],
        body=serialized_data["body"],
        owner=current_user
        )
    template_obj.save()
    return jsonify({
        "status": "success",
        "msg": "Template created successfully"
    }), 201



@temp.route('/<id>', methods=["GET"])
@jwt_required()
def get_template(id):
    template = Template.objects(id=id).first()
    if template:
        if template.owner.id == current_user.id:
            serializer = TemplateSchema(exclude=('owner',)).dump(template)
            return jsonify({
                "status": "success",
                "template": serializer
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "msg": "You are not permitted to access this resource"
            }), 403
    return jsonify({
                "status": "failed",
                "msg": "The requested template was not found"
            }), 404



@temp.route('', methods=["GET"])
@jwt_required()
def get_templates():
    templates = Template.objects(owner=current_user.id).all()
    serializer = TemplateSchema(many=True,exclude=('owner',))
    return jsonify({
        "status":"success",
        "templates": serializer.dump(templates)
    }), 200




@temp.route('/<id>', methods=["PUT"])
@jwt_required()
def update_template(id):
    data = request.get_json()
    template = Template.objects(id=id).first()
    if template:
        if template.owner.id == current_user.id:
            serializer = TemplateSchema(exclude=('owner',))
            serialized_data = serializer.load(data, partial=True)
            template.template_name = serialized_data.get('template_name', template.template_name)
            template.subject = serialized_data.get('subject', template.subject)
            template.body = serialized_data.get('body', template.body)
            template.modified_on = datetime.utcnow()
            template.save()
            return jsonify({
                "status": "success",
                "template": serializer.dump(template)
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "msg": "You are not permitted to update this resource"
            }), 403
    return jsonify({
                "status": "failed",
                "msg": "The requested template was not found"
            }), 404


@temp.route('/<id>', methods=["DELETE"])
@jwt_required()
def delete_template(id):
    template = Template.objects(id=id).first()
    if template:
        if template.owner.id == current_user.id:
            template.delete()
            return jsonify({
                "status": "success",
                "msg": "Template deleted successfully"
            }), 200
        else:
            return jsonify({
                "status": "failed",
                "msg": "You are not permitted to delete this resource"
            }), 403
    return jsonify({
                "status": "failed",
                "msg": "The requested template was not found"
            }), 404

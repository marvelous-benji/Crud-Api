import uuid
from datetime import datetime

from project import db, bcrypt

from marshmallow import Schema, fields, validate


def hex_id():
    """
    generates unique and random ids
    for primary key usage
    """

    return uuid.uuid4().hex


class User(db.Document):
    """
    An object document mapping of the User document.
    """

    id = db.StringField(max_lenght=50, primary_key=True, default=hex_id)
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50, required=True)
    email = db.EmailField(max_lenght=80, required=True, unique=True)
    password = db.StringField(max_lenght=140, required=True)
    date_created = db.DateTimeField(default=datetime.utcnow)

    def __repr__(self):
        """
        A readable representation of the User class
        """

        return f"User('{self.id}','{self.email}')"

    @staticmethod
    def hash_password(password):

        return bcrypt.generate_password_hash(password).decode()

    @staticmethod
    def verify_password_hash(password_hash, password):
        """
        Verifies that user password is correct
        """

        return bcrypt.check_password_hash(password_hash, password)


class UserSchema(Schema):
    """
    A serializer schema for the User document
    """

    class Meta:
        model = User
        ordered = True

    id = fields.String(dump_only=True)
    first_name = fields.String(validate=validate.Length(min=3), required=True)
    last_name = fields.String(validate=validate.Length(min=3), required=True)
    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=7), load_only=True)
    date_created = fields.DateTime(dump_only=True)


class Template(db.Document):
    """
    An object document mapping of the Template document.
    """

    id = db.StringField(max_lenght=50, primary_key=True, default=hex_id)
    template_name = db.StringField(max_length=100, required=True)
    subject = db.StringField(max_length=80, required=True)
    body = db.StringField()
    created_on = db.DateTimeField(default=datetime.utcnow)
    modified_on = db.DateTimeField(defaut=datetime.utcnow)
    owner = db.ReferenceField(User)

    def __repr__(self):
        """
        A readable representation of the Template class
        """

        return f"Template('{self.subject}','{self.owner.email}')"


class TemplateSchema(Schema):
    """
    A serializer schema for the Template document
    """

    class Meta:
        model = Template
        ordered = True

    id = fields.String(dump_only=True)
    template_name = fields.String(required=True)
    subject = fields.String(required=True)
    body = fields.String(required=True)
    created_on = fields.DateTime(dump_only=True)
    modified_on = fields.DateTime(dump_only=True)
    owner = fields.Nested(UserSchema(only=("id", "email")))

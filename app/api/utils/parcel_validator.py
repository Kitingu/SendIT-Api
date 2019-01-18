from marshmallow import Schema, fields, ValidationError
from flask_restplus import reqparse, inputs
import re


def validate_length(input):
    if input.strip() == '':
        raise ValidationError('fields cannot be blank')
    elif not re.match(r"^(?=.*[a-z])[a-zA-Z0-9_.-]{3,25}$", input):
        raise ValidationError("{} is not a valid input".format(input))


def validate_weight(weight):
    if weight <= 0:
        raise ValidationError("please provide valid weight")


def validate_password(password):
    if not re.match('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$<>~$%^&*()_+])', password):
        raise ValidationError(
            "password should at least have an uppercase,lowercase,number and a special character")


def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        raise ValidationError("please enter a valid email address")


class ParcelSchema(Schema):
    sender_name = fields.String(required=True, validate=validate_length)
    receiver_name = fields.String(required=True, validate=validate_length)
    receiver_contact = fields.Email(required=True, validate=validate_email)
    weight = fields.Int(required=True, validate=validate_weight)
    pickup_location = fields.String(required=True, validate=validate_length)
    destination = fields.String(required=True, validate=validate_length)


class UserSchema(Schema):
    username = fields.String(required=True, validate=validate_length)
    email = fields.Email(required=True, validate=validate_email)
    password = fields.String(required=True, validate=validate_password)


class LoginSchema(Schema):
    email = fields.String(required=True, validate=validate_email)
    password = fields.String(required=True)


class DestinationSchema(Schema):
    destination = fields.String(required=True, validate=validate_length)


class LocationSchema(Schema):
    location = fields.String(required=True, validate=validate_length)


class StatusSchema(Schema):
    status = fields.String(required=True, validate=validate_length)


def validator(schema, error_types, data):
    result = schema.load(data)
    errors = result.errors
    for error in error_types:
        if error in errors.keys():
            return {'message': {error: errors[error][0]}}, 400

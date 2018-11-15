from marshmallow import Schema, fields, ValidationError
from flask_restplus import reqparse, inputs
import re

def validate_length(input):
    if input.strip() == '':
        raise ValidationError('fields cannot be blank')
    elif not re.match(r"^(?=.*[a-z])[a-zA-Z0-9_.-]{3,25}$", input):
        raise ValidationError("{} is not a valid input".format(input))

def validate_weight(weight):
    if weight < 0:
        raise ValidationError("please provide valid weight")

def validate_password(password):
    if not re.match(r'[A-Za-z0-9_@#$%^&\*+=,\.`\-]{6,}',password):
        raise ValidationError("please should provide a strong password")


class ParcelSchema(Schema):
    sender_name = fields.String(required=True, validate=validate_length)
    receiver_name = fields.String(required=True, validate=validate_length)
    receiver_contact = fields.Email(required=True)
    weight = fields.Integer(required=True, validate=validate_weight)
    pickup_location = fields.String(required=True, validate=validate_length)
    destination = fields.String(required=True, validate=validate_length)


class UserSchema(Schema):
    username = fields.String(required=True, validate=validate_length)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate_password)


class LoginParser:
    parser = reqparse.RequestParser()

    parser.add_argument('password',
                        type=str,
                        required=True,
                        location='json',
                        help="This field cannot be blank")

    parser.add_argument('email',
                        type=inputs.regex(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'),
                        required=True,
                        location='json',
                        help="please enter a valid email")


class DestinationParser:
    parser = reqparse.RequestParser()
    parser.add_argument('destination',
                        type=str,
                        required=True,
                        location='json',
                        help='input a valid destination')

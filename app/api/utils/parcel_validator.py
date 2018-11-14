from marshmallow import Schema, fields, ValidationError
from flask_restplus import reqparse, inputs


def validate_length(input):
    if input.strip() == '':
        raise ValidationError('fields cannot be blank')
    elif len(input) < 3:
        raise ValidationError("{} is not a valid input".format(input))


def validate_weight(weight):
    if weight < 0:
        raise ValidationError("please provide valid weight")


class ParcelSchema(Schema):
    sender_name = fields.String(required=True, validate=validate_length)
    receiver_name = fields.String(required=True, validate=validate_length)
    receiver_contact = fields.Email(required=True)
    weight = fields.Integer(required=True, validate=validate_weight)
    pickup_location = fields.String(required=True, validate=validate_length)
    destination = fields.String(required=True, validate=validate_length)


class UserSchema(Schema):
    username = fields.String(required=True, validate=validate_length)
    email = fields.Email(required=True, validate=validate_length)
    password = fields.String(required=True, validate=validate_length)


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
                        help="please enter a valid date")


class DestinationParser:
    parser = reqparse.RequestParser()
    parser.add_argument('destination',
                        type=str,
                        required=True,
                        location='json',
                        help='input a valid destination')

from marshmallow import Schema, fields, validates, ValidationError


class ParcelSchema(Schema):
    sender_name = fields.String(required=True, )
    receiver_name = fields.String(required=True)
    receiver_contact = fields.Email(required=True)
    weight = fields.Integer(required=True)
    pickup_location = fields.String(required=True)
    destination = fields.String(required=True)

    @validates('sender_name')
    def validates_sender(self, sender_name):
        if sender_name.strip() == '':
            raise ValidationError('sender_name cannot be blank')
        elif len(sender_name) < 3:
            raise ValidationError("please provide a valid name")

    @validates('receiver_name')
    def validates_receiver_name(self, receiver_name):
        if receiver_name.strip() == '':
            raise ValidationError('receive cannot be blank')
        elif len(receiver_name) < 3:
            raise ValidationError("please provide a valid name")

    @validates('weight')
    def validates_weight(self, weight):
        if weight < 0:
            raise ValidationError("please provide valid weight")

    @validates('pickup_location')
    def validates_pickup_location(self, pickup_location):
        if pickup_location.strip() == '':
            raise ValidationError('please provide valid pickup_location')
        elif len(pickup_location) < 3:
            raise ValidationError("please provide valid pickup_location")

    @validates('destination')
    def validates_destination(self, destination):
        if destination.strip() == '':
            raise ValidationError('please provide valid destination')
        elif len(destination) < 3:
            raise ValidationError("please provide valid destination")
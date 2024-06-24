from wtforms import Form, StringField, validators
from wtforms.validators import ValidationError


def at_least_one_filled(form, field):
    if not form.phone_number.data and not form.email_address.data:
        raise ValidationError('Either phone number or email address must be provided.')


class OrderForm(Form):
    """A form representing new Order"""

    first_name = StringField(
        "First Name",
        [validators.DataRequired("Product Quantity is required!")],
    )

    middle_name = StringField(
        "Sur Name",
        [],
    )

    last_name = StringField(
        "Last Name",
        [validators.DataRequired("Last Name is required!")],
    )

    street_address = StringField(
        "Street Address",
        [validators.DataRequired("Street Address is required!")],
    )
    city = StringField(
        "City",
        [validators.DataRequired("City is required!")],
    )
    zip_code = StringField(
        "Zip Code",
        [validators.DataRequired("Zip Code is required!")],
    )
    state_or_province = StringField(
        "State or Province",
        [validators.DataRequired("State or Province is required!")],
    )
    email_address = StringField(
        "Email Address",
        [validators.Optional(), at_least_one_filled, validators.Email()],
    )
    phone_number = StringField(
        "Phone Number",
        [validators.Optional(), at_least_one_filled],
    )

    mpesa_number = StringField(
        "Mpesa Number",
        [validators.DataRequired("Mpesa Mobile Number Required"), at_least_one_filled],
    )

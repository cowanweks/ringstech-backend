from wtforms import Form, StringField, validators


class OrderForm(Form):
    """A form representing new Order"""

    product_id = StringField(
        "Product ID", [validators.DataRequired("Product ID is required!")]
    )
    quantity = StringField(
        "Product Quantity to be purchased",
        [validators.DataRequired("Product Quantity is required!")],
    )

    shipping_address = StringField(
        "Shipping Address",
        [validators.DataRequired("Shipping Address is required!")],
    )

    color = StringField(
        "Product Color",
        [validators.DataRequired("Product Color is required!")],
    )

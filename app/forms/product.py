from wtforms import Form, StringField, validators, BooleanField, IntegerField, FileField


class ProductForm(Form):
    """A form representing Product registration"""

    in_stock = IntegerField(
        "Product in Stock", [validators.DataRequired("Product in Stock required!")]
    )
    brand = StringField(
        "Product Brand", [validators.DataRequired("Product Brand is required!")]
    )
    model = StringField("Product Model", [validators.DataRequired("Product Model is required!")])
    battery = StringField("Product Battery", [])
    cameras = StringField("Product Cameras", [])
    product_image = FileField("Product Image", [])
    processor = StringField("Product Processor", [])
    display = StringField("Product Display", [])
    ram = StringField("Product RAM", [])

    product_name = StringField(
        "Product Name", [validators.DataRequired("Product Name is required!")]
    )
    product_unit_price = StringField(
        "Product Unit Price",
        [validators.DataRequired("Product Unit Price is required!")],
    )

    description = StringField(
        "Product Description",
        [validators.DataRequired("Product Description is required!")],
    )
    product_category = StringField(
        "Product Category", [validators.DataRequired("Product Category is required!")]
    )

    available_colors = StringField(
        "Available Color",
        [validators.DataRequired("Product Available Colors is required!")],
    )

    is_available = BooleanField(
        "Product Is Available",
        [],
    )


class ProductUpdateForm(Form):
    """A form representing Product update"""

    product_id = StringField(
        "Product ID", [validators.DataRequired("Product ID is required!")]
    )
    product_name = StringField(
        "Product Name", [validators.DataRequired("Product Name is required!")]
    )
    product_unit_price = StringField(
        "Product Unit Price",
        [validators.DataRequired("Product Unit Price is required!")],
    )

    description = StringField(
        "Product Description",
        [validators.DataRequired("Product Description is required!")],
    )
    product_category = StringField(
        "Product Category", [validators.DataRequired("Product Category is required!")]
    )

    available_colors = StringField(
        "Available Color",
        [validators.DataRequired("Product Available Colors is required!")],
    )

    is_available = BooleanField(
        "Product Is Available",
        [validators.DataRequired("Product Availability is required!")],
    )

import base64
import json
import datetime
from dataclasses import dataclass
from sqlalchemy.types import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .extensions import db
from sqlalchemy import LargeBinary
import io

@dataclass
class Users(db.Model):
    """Model Representing Users"""

    user_id: Mapped[str] = mapped_column(db.String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(db.String(), unique=True)
    email: Mapped[str] = mapped_column(db.String(), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(db.String(), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(db.String())
    roles: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "user_id": self.user_id,
            "customer_id": self.customer_id,
            "password": self.password,
            "username": self.username,
            "email": self.email,
            "role": self.roles,
        }


@dataclass
class Address(db.Model):
    """Model Representing Users"""

    address_id: Mapped[str] = mapped_column(db.String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(db.String(), unique=True)
    street_address: Mapped[str] = mapped_column(db.String())
    address_line_2: Mapped[str] = mapped_column(db.String())
    city: Mapped[str] = mapped_column(db.String())
    state: Mapped[str] = mapped_column(db.String())
    postal_code: Mapped[str] = mapped_column(db.String())
    country: Mapped[str] = mapped_column(db.String())
    phone_number: Mapped[str] = mapped_column(db.String())
    email_address: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "address_id": self.address_id,
            "customer_id": self.customer_id,
            "email_address": self.email_address,
            "address_line_2": self.address_line_2,
            "street_address": self.street_address,
            "city": self.city,
            "country": self.country,
            "phone_number": self.phone_number,
            "postal_code": self.postal_code,
            "state": self.state,
        }


@dataclass
class ShippingAddress(Address):
    """Model Representing Shipping Address"""

    __tablename__ = "shipping_addresses"

    full_name: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "full_name": self.full_name,
            "address_id": self.address_id,
            "customer_id": self.customer_id,
            "email_address": self.email_address,
            "address_line_2": self.address_line_2,
            "street_address": self.street_address,
            "city": self.city,
            "country": self.country,
            "phone_number": self.phone_number,
            "postal_code": self.postal_code,
            "state": self.state,
        }


@dataclass
class Customer(db.Model):
    """Model Representing Users"""

    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(db.String, primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String())
    middle_name: Mapped[str] = mapped_column(db.String())
    last_name: Mapped[str] = mapped_column(db.String())
    phone: Mapped[str] = mapped_column(db.String())
    email: Mapped[str] = mapped_column(db.String())
    address: Mapped[str] = mapped_column(db.String)
    shipping_address: Mapped[str] = mapped_column(db.String)
    reg_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )

    def serialize(self):
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "shipping_address": self.shipping_address,
            "reg_date": self.reg_date,
        }


class Image(db.Model):
    """Model representing images"""

    __tablename__ = 'images'

    id = db.Column(db.Text, primary_key=True)
    image_name = db.Column(db.Text, unique=True, nullable=False)
    image = db.Column(LargeBinary, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


@dataclass
class Product(db.Model):
    """Model Representing Staffs"""

    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(db.String(), primary_key=True)
    product_name: Mapped[str] = mapped_column(db.String(), nullable=False)
    product_unit_price: Mapped[str] = mapped_column(db.String(), nullable=False)
    description: Mapped[str] = mapped_column(db.String(), nullable=False)
    product_category: Mapped[str] = mapped_column(db.String(), nullable=False)
    available_colors: Mapped[str] = mapped_column(db.String())
    is_available: Mapped[bool] = mapped_column(db.Boolean())
    in_stock: Mapped[int] = mapped_column(db.Integer)
    product_image: Mapped[str] = mapped_column(db.String, nullable=False)
    model: Mapped[str] = mapped_column(db.String, nullable=False)
    brand: Mapped[str] = mapped_column(db.String, nullable=False)
    battery: Mapped[str] = mapped_column(db.String, nullable=False)
    cameras: Mapped[str] = mapped_column(db.String, nullable=False)
    processor: Mapped[str] = mapped_column(db.String, nullable=False)
    display: Mapped[str] = mapped_column(db.String, nullable=False)
    ram: Mapped[str] = mapped_column(db.String, nullable=False)

    @property
    def available_colors_list(self):
        if self.available_colors:
            return json.loads(self.available_colors)
        return []

    @available_colors_list.setter
    def available_colors_list(self, value):
        self.available_colors = json.dumps(value)

    def serialize(self):
        return {
            "productID": self.product_id,
            "productName": self.product_name,
            "unitPrice": self.product_unit_price,
            "description": self.description,
            "productCategory": self.product_category,
            "availableColors": self.available_colors,
            "isAvailable": self.is_available,
            "inStock": self.in_stock,
            "productImage": self.product_image,
            "brand": self.brand,
            "model": self.model,
            "battery": self.battery,
            "cameras": self.cameras,
            "processor": self.processor,
            "display": self.display,
            "ram": self.ram
        }


@dataclass
class Order(db.Model):
    """Model representing an order"""

    __tablename__ = "orders"

    order_id: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    color: Mapped[str] = mapped_column(db.String)
    product_id: Mapped[str] = mapped_column(db.String)
    quantity: Mapped[int] = mapped_column(db.Integer)
    shipping_address: Mapped[str] = mapped_column(db.String)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )

    def serialize(self):
        return {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "color": self.color,
            "created_at": self.created_at,
            "shipping_address": self.shipping_address,
        }


@dataclass
class Roles(db.Model):
    """Model Representing Roles available to registered users"""

    __tablename__ = "roles"

    role_id: Mapped[str] = mapped_column(db.String, primary_key=True, nullable=False)
    role_name: Mapped[str] = mapped_column(db.String(), unique=True, nullable=False)
    role_description: Mapped[str] = mapped_column(db.String())

    def serialize(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
        }

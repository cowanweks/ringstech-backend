from uuid import uuid4
from werkzeug.datastructures import MultiDict
from app.models import db, Product
from app.forms.product import ProductForm, ProductUpdateForm
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import requests


def new_product(form: dict, file_name: str):
    """A controller that handles new user registrations"""

    try:
        new_product_form = ProductForm(form)

        if new_product_form.validate():

            product = Product(
                product_id=str(uuid4()),
                product_name=new_product_form.product_name.data,
                available_colors=new_product_form.available_colors.data,
                product_category=new_product_form.product_category.data,
                description=new_product_form.description.data,
                is_available=new_product_form.is_available.data,
                product_unit_price=new_product_form.product_unit_price.data,
                product_image=file_name,
                in_stock=new_product_form.in_stock.data,
                battery=new_product_form.battery.data,
                cameras=new_product_form.cameras.data,
                display=new_product_form.display.data,
                processor=new_product_form.processor.data,
                gamesIncluded=new_product_form.gamesIncluded.data,
                ram=new_product_form.ram.data,
                brand=new_product_form.brand.data,
                model=new_product_form.model.data,
            )

            db.session.add(product)
            db.session.commit()
            return True, "Successfully Created new Product!"

        else:
            print(new_product_form.errors)
            return False, new_product_form.errors

    except IntegrityError as ex:
        print(ex)
        return False, "Product already exists!"


def get_products(args: MultiDict[str, str]):
    """A controller that handles getting Products"""

    product_id = args.get("product_id")
    product_category = args.get("product_category")

    try:
        query = db.select(Product).order_by(Product.product_id)

        if product_id:
            query = query.where(Product.product_id == product_id)
        if product_category:
            query = query.where(Product.product_category == product_category)

        products = db.session.execute(query).scalars().all()
        serialized_products = [product.serialize() for product in products]
        return True, serialized_products

    except Exception as ex:
        print(ex)
        return False, "Database error occurred!"


def update_product(product_id: str, data: dict):
    """Update user"""
    try:
        updated_product_form = ProductUpdateForm(data)

        if updated_product_form.validate():
            db.session.execute(
                db.update(Product)
                .where(Product.product_id == product_id)
                .values(
                    product_id=updated_product_form.product_id.data,
                    product_name=updated_product_form.product_name.data,
                )
            )
            db.session.commit()
            return True, "Successfully Updated Product!"

        else:
            return False, updated_product_form.errors

    except SQLAlchemyError as ex:
        print(ex)
        return False, "Database error occurred!"


def delete_product(product_id: str):
    """A controller that Deletes user"""
    try:
        db.session.execute(db.delete(Product).where(Product.product_id == product_id))
        db.session.commit()
        db.session.close()
        return True, "Successfully Deleted Product!"

    except SQLAlchemyError as ex:
        print(ex)
        db.session.close()
        return False, "Database error occurred!"

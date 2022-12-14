from flask_wtf.file import file_allowed, FileField, file_required
from wtforms import Form, StringField, BooleanField, TextAreaField, IntegerField, validators, DecimalField
class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colours = TextAreaField('Colours', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[file_allowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Image 2', validators=[file_allowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Image 3', validators=[file_allowed(['jpg', 'png', 'gif', 'jpeg'])])


    
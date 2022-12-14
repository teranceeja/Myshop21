from logging import WARNING
from sre_constants import SUCCESS
from unicodedata import category
from flask import redirect, render_template, url_for, request, flash, session, current_app
from shop import db, app, photos, search
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os


def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
      categories = Category.query.join(Addproduct, (Category.id ==Addproduct.category_id)).all()
      return categories



@app.route('/')
def Home():
    page = request.args.get('page',1, type=int) 
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=8)
    return render_template('products/index.html', products=products, brands=brands(), categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product, brands=brands(), categories=categories())

@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name', 'desc'], limit=3 )
    return render_template('products/result.html', products=products, brands=brands(), categories=categories())


@app.route('/brand/<int:id>')
def get_brand(id):
    get_b = Brand.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    brand = Addproduct.query.filter_by(brand=get_b).paginate(page=page, per_page=6)
   
    return render_template('products/index.html', brand=brand, brands=brands(), categories=categories(), get_b=get_b)

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=6)
    return render_template('products/index.html',  categories= categories(), get_cat_prod=get_cat_prod ,  brands= brands(), get_cat=get_cat)



@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to the database', 'success')
        db.session.commit()
        return redirect(url_for ('addbrand'))
    
    return render_template('products/addbrand.html', brands='brands')



@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email'not in session:
        flash(f'please login first', 'danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', tittle='Update brand page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', WARNING)
        return redirect(url_for('admin'))







@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email'not in session:
        flash(f'please login first', 'danger')
    updatecat= Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = category
        flash(f'Your Category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', tittle='Update Category page', updatecat=updatecat)

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    cat = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'The Category {category.name} was deleted from your database', WARNING)
        return redirect(url_for('admin'))




@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    categories = Category.query.all()
    brands = Brand.query.all()
    product = Addproduct.query.get_or_404(id)
    form = Addproducts(request.form)
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.category_id = category
        product.colours = form.colours.data
        product.desc = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                 product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                 product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                 product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Your product has been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colours.data = product.colours
    form.description.data = product.desc




    return render_template('products/updateproduct.html', form=form, product=product, categories=categories, brands=brands, brand=brand)


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if request.method == "POST":
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} was added to the database', 'success')
        db.session.commit()
        return redirect(url_for ('addcat'))
    
    return render_template('products/addbrand.html')


@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colours = form.colours.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')


        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock,colours=colours, desc=desc, 
        brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3 )
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()

        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', tittle="Add product page", form=form, brands=brands, categories= categories)

@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):

    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f'the product {product.name} was deleted from your record', SUCCESS)
        return redirect(url_for('admin'))
    flash(f"can't delete the product", 'danger')

    return redirect(url_for('admin'))
    


    
      


        
           
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
db = SQLAlchemy(app)


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }



class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course
        }


# ========================= Restaurants Part

@app.route('/')
@app.route('/restaurants')
def index():
    restaurants = Restaurant.query.all()
    return render_template('index.html', restaurants=restaurants)


@app.route('/restaurants/new', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        rest_name = request.form['rest_name']
        new_restaurant = Restaurant(name=rest_name)

        try:
            db.session.add(new_restaurant)
            db.session.commit()
            flash('new restaurant created!')
            return redirect('/')
        except:
            return 'Something wrong is going on'

    else:
        return render_template('new.html')


@app.route('/restaurants/<int:id>/delete', methods=['POST', 'GET'])
def delete(id):
    restaurant_to_delete = Restaurant.query.get_or_404(id)

    if request.method == 'POST':

        try:
            db.session.delete(restaurant_to_delete)
            db.session.commit()
            flash('restaurant deleted!')
            return redirect('/')
        except:
            return 'Something wrong is going on'

    else:
        return render_template('delete.html', restaurant=restaurant_to_delete)


@app.route('/restaurants/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    restaurant_to_edit = Restaurant.query.get_or_404(id)

    if request.method == 'POST':
        restaurant_to_edit.name = request.form['rest_name']

        try:
            db.session.commit()
            flash('restaurant edited!')
            return redirect('/')
        except:
            return 'Something wrong is going on'

    else:
        return render_template('edit.html', restaurant=restaurant_to_edit)


@app.route('/restaurants/JSON')
def restaurants_json():
    restaurants_to_json = Restaurant.query.all()

    return jsonify(restaurants=[rest.serialize for rest in restaurants_to_json])


# ========================= Menu Part

@app.route('/restaurants/<int:restaurant_id>/menu')
def menu(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()

    return render_template('/menu/menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/restaurants/<int:restaurant_id>/new_menu_item', methods=['POST', 'GET'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        item_name = request.form['item_name']
        new_menu_item = MenuItem(name=item_name, restaurant_id=restaurant_id)

        try:
            db.session.add(new_menu_item)
            db.session.commit()
            flash('new menu item created!')
            return redirect(url_for('menu', restaurant_id=restaurant_id))
        except:
            return 'Something wrong is going on'

    else:
        return render_template('/menu/new_item.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>', methods=['POST', 'GET'])
def edit_menu_item(restaurant_id, menu_id):
    item_to_edit = MenuItem.query.get_or_404(menu_id)

    if request.method == 'POST':
        item_to_edit.name = request.form['item_name']

        try:
            db.session.commit()
            flash('menu item edited!')
            return redirect(url_for('menu', restaurant_id=restaurant_id))
        except:
            return 'Something wrong is going on'

    else:
        return render_template('/menu/edit_item.html', restaurant_id=restaurant_id, item=item_to_edit)


@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>', methods=['POST', 'GET'])
def delete_menu_item(restaurant_id, menu_id):
    item_to_delete = MenuItem.query.get_or_404(menu_id)

    if request.method == 'POST':

        try:
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('menu item deleted!')
            return redirect(url_for('menu', restaurant_id=restaurant_id))
        except:
            return 'Something wrong is going on'

    else:
        return render_template('/menu/delete_item.html', restaurant_id=restaurant_id, item=item_to_delete)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()

    return jsonify(menu_items=[item.serialize for item in menu_items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
    item_to_json = MenuItem.query.get_or_404(menu_id)

    return jsonify(menu_item=item_to_json.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
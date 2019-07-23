from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
db = SQLAlchemy(app)


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)


class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)


@app.route('/restaurants/<int:restaurant_id>/')
def index(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id)

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/<int:restaurant_id>/new_menu_item')
def new_menu_item(restaurant_id):
    return 'page to create new menu item'


@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>')
def edit_menu_item(restaurant_id, menu_id):
    return 'page to edit a new menu item'


@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>')
def delete_menu_item(restaurant_id, menu_id):
    return 'page to delete a new menu item'


if __name__ == '__main__':
    app.run(debug=True)
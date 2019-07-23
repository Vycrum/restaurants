from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
db = SQLAlchemy(app)


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'


@app.route('/')
def index():
    restaurants = Restaurant.query.all()
    return render_template('index.html', restaurants=restaurants)


@app.route('/new', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        rest_name = request.form['rest_name']
        new_restaurant = Restaurant(name=rest_name)

        try:
            db.session.add(new_restaurant)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something wrong is going on'

    else:
        return render_template('new.html')


@app.route('/<int:id>/delete', methods=['POST', 'GET'])
def delete(id):
    restaurant_to_delete = Restaurant.query.get_or_404(id)

    if request.method == 'POST':

        try:
            db.session.delete(restaurant_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something wrong is going on'

    else:
        return render_template('delete.html', restaurant=restaurant_to_delete)


@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit(id):
    restaurant_to_edit = Restaurant.query.get_or_404(id)

    if request.method == 'POST':
        restaurant_to_edit.name = request.form['rest_name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Something wrong is going on'

    else:
        return render_template('edit.html', restaurant=restaurant_to_edit)

if __name__ == "__main__":
    app.run(debug=True)
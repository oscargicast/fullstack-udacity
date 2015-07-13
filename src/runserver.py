from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Making an API Endpoint (Get Request).
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def RestaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON/')
def MenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id,
        id=menu_id,
    ).one()
    return jsonify(MenuItems=item.serialize)


@app.route('/')
@app.route('/restaurants/')
def Restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template(
        'restaurants.html',
        restaurants=restaurants,
    )


@app.route('/restaurants/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template(
        'menu.html',
        restaurant=restaurant,
        items=items,
    )


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def NewMenuItem(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=request.form.get('price'),
            course=request.form.get('course'),
            restaurant_id=restaurant_id,
        )
        session.add(new_item)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for(
            'RestaurantMenu',
            restaurant_id=restaurant_id,
        ))
    else:
        return render_template(
            'new-menu-item.html',
            restaurant_id=restaurant_id,
        )


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def EditMenuItem(restaurant_id, menu_id):
    edited_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        edited_item.name = request.form.get('name')
        edited_item.description = request.form.get('description')
        edited_item.price = request.form.get('price')
        edited_item.course = request.form.get('course')
        session.add(edited_item)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for(
            'RestaurantMenu',
            restaurant_id=restaurant_id,
        ))
    else:
        return render_template(
            'edit-menu-item.html',
            item=edited_item,
        )


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def DeleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for(
            'RestaurantMenu',
            restaurant_id=restaurant_id,
        ))
    else:
        return render_template(
            'delete-menu-item.html',
            item=item,
        )


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

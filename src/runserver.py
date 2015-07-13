from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


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
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            course=request.form['course'],
            restaurant_id=restaurant_id,
        )
        session.add(new_item)
        session.commit()
        return redirect(url_for(
            'RestaurantMenu',
            restaurant_id=restaurant_id,
        ))
    else:
        return render_template(
            'new-menu-item.html',
            restaurant_id=restaurant_id,
        )


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def EditMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def DeleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

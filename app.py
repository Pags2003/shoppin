from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class dbaccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class dbcart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    types = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class dbitems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discounted_price = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(200), nullable=False)
    types = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


class dborders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    payment = db.Column(db.String(200), nullable=False)
    order_total = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('adminfront.html')


@app.route('/users')
def users():
    data = dbaccount.query.order_by(dbaccount.username).all()
    return render_template('adminuser.html', users=data)


@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    # cursor = mysql.connection.cursor()
    # cursor.execute("DELETE FROM account WHERE id=%s", (id,))
    # mysql.connection.commit()
    # cursor.close()
    _user = dbaccount.query.get_or_404(id)
    flash('User deleted successfully!')
    try:
        db.session.delete(_user)
        db.session.commit()
    except:
        msg = 'There was a problem deleting that task'
    return redirect('/users')


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    #     cursor = mysql.connection.cursor()
    #     cursor.execute("DELETE FROM items WHERE id=%s", (id,))
    flash('Item deleted successfully!')
#     mysql.connection.commit()
#     cursor.close()
    _items = dbitems.query.get_or_404(id)
    try:
        db.session.delete(_items)
        db.session.commit()
    except:
        msg = 'There was a problem deleting that task'
    return redirect('/items')


@app.route('/newitem', methods=['GET', 'POST'])
def newitem():
    msg = ''
    if request.method == 'POST' and 'image' in request.form and 'name' in request.form and 'price' in request.form and 'dprice' in request.form and 'colour' in request.form and 'types' in request.form and 'category' in request.form:
        _image = request.form['image']
        _name = request.form['name']
        _price = request.form['price']
        _dprice = request.form['dprice']
        _colour = request.form['colour']
        _types = request.form['types']
        _category = request.form['category']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute(
        #     'SELECT * FROM items WHERE name = % s', (name, ))
        # account = cursor.fetchone()
        _item = dbitems.query.filter_by(name=_name).first()
        if _item:
            msg = 'Item already present !'
        elif not _name or not _image or not _price or not _dprice or not _colour or not _types or not _category:
            msg = 'Please fill all boxes !'
        else:
            # cursor.execute(
            #     'INSERT INTO items VALUES (NULL, % s, % s, % s, % s, % s, % s, % s)', (image, name, price, dprice, colour, types ,category, ))
            # mysql.connection.commit()
            try:
                new_item = dbitems(image=_image,
                                   name=_name,
                                   price=_price,
                                   discounted_price=_dprice,
                                   color=_colour,
                                   types=_types,
                                   category=_category)
                db.session.add(new_item)
                db.session.commit()
                msg = 'Item Added !'
            except:
                msg = 'There was an error'
    elif request.method == 'POST':
        msg = 'Please fill boxes !'
    return render_template('newitem.html', msg=msg)


@app.route('/index/additem/<int:id>')
def additemfront(id):
    # cursor = mysql.connection.cursor()
    # cursor.execute(
    #     "INSERT INTO cart (image,name,price,type) SELECT image, name,`discounted price`, type FROM items WHERE id=%s", (id,))
    # mysql.connection.commit()
    _item = dbitems.query.filter_by(id=id).first()
    try:
        new_item = dbcart(image=_item.image,
                          name=_item.name,
                          price=_item.discounted_price,
                          types=_item.types)
        db.session.add(new_item)
        db.session.commit()
        msg = 'Item Added to cart!'
    except:
        msg = 'There was an error'
    return render_template('index.html')


@app.route('/additem/<int:id>')
def additem(id):
    # cursor = mysql.connection.cursor()
    # cursor.execute(
    #     "INSERT INTO cart (image,name,price,type) SELECT image, name,`discounted price`, type FROM items WHERE id=%s", (id,))
    # mysql.connection.commit()
    # cursor.execute("SELECT category FROM items WHERE id=%s", (id,))
    _item = dbitems.query.filter_by(id=id).first()
    category = _item.category
    new_item = dbcart(image=_item.image,
                      name=_item.name,
                      price=_item.discounted_price,
                      types=_item.types)
    db.session.add(new_item)
    db.session.commit()
    msg = 'Item Added to cart!'

    if category == 'men':
        # cursor.execute('SELECT * FROM items WHERE category = "men"')
        # data = cursor.fetchall()
        # cursor.close()
        data = dbitems.query.filter_by(category='men').all()
        # return render_template('items.html', items=data ,category = 'men' )
        return redirect('/men')
    elif category == 'women':
        # cursor.execute('SELECT * FROM items WHERE category = "women"')
        # data = cursor.fetchall()
        # cursor.close()
        return redirect('/women')
        data = dbitems.query.filter_by(category='women').all()
        # return render_template('items.html', items=data,category = 'women')
    else:
        # cursor.execute('SELECT * FROM items WHERE category = "child"')
        # data = cursor.fetchall()
        # cursor.close()
        data = dbitems.query.filter_by(category='child').all()
        return redirect('/child')
        # return render_template('items.html', items=data,category = 'child')


@app.route('/removeitem/<int:id>')
def removeitem(id):
    # cursor = mysql.connection.cursor()
    # cursor.execute("DELETE FROM cart WHERE id=%s", (id,))
    flash('Item deleted successfully!')
    # mysql.connection.commit()
    # cursor.close()
    _items = dbcart.query.get_or_404(id)
    try:
        db.session.delete(_items)
        db.session.commit()
    except:
        msg = 'There was a problem'
    return redirect('/cart')


@app.route('/orders')
def orders():

    data = dborders.query.order_by(dborders.date_created).all()
    return render_template('adminorders.html', orders=data)


@app.route('/updatestatus/<int:id>')
def updatestatus(id):
    # cursor = mysql.connection.cursor()
    # cursor.execute("UPDATE `htmlproject`.`orders` SET `status` = 'Delivered' WHERE (`id` = %s );", (id,))
    # mysql.connection.commit()
    # cursor.close()
    _order = dborders.query.filter_by(id=id).first()

    _date_created = _order.date_created
    _payment = _order.payment
    _order_total = _order.order_total
    _address = _order.address
    try:
        db.session.delete(_order)

        new_item = dborders(date_created=_date_created,
                            payment=_payment,
                            order_total=_order_total,
                            address=_address,
                            status='Delivered')
        db.session.add(new_item)
        db.session.commit()
        msg = 'Status Updated !'

    except:
        msg = 'There was a problem updating status'

    return redirect('/orders')


@app.route('/cart')
def cart():
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM cart')
    # data = cursor.fetchall()
    # cursor.execute('SELECT SUM(price) FROM cart')
    # total = cursor.fetchall()
    # cursor.close()
    _sum = 0
    _items = dbcart.query.order_by(dbcart.name).all()
    for _item in _items:
        _sum = _sum + _item.price
    session['total'] = _sum
    return render_template('cart.html', items=_items, total=_sum)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    total = session['total']
    msg = ''
    if request.method == 'POST' and 'payment' in request.form and 'address' in request.form:
        _payment = request.form['payment']
        _address = request.form['address']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not _address or not _payment:
            msg = 'Please fill all boxes !'
            return render_template('checkout.html', total=total, msg=msg)
        else:
            _status = 'Not delivered'
            try:
                new_item = dborders(payment=_payment,
                                    order_total=total,
                                    address=_address,
                                    status=_status)
                db.session.add(new_item)
                db.session.commit()
                msg = 'Order placed'
                return render_template('index.html')

            except:
                msg = 'Problem occured in placing order'
                return render_template('checkout.html', total=total, msg=msg)
            # cursor.execute(
            #     'INSERT INTO orders VALUES (NULL, % s, %s, % s, % s,  % s)', (x, payment, total, address, status, ))
            # cursor.execute('TRUNCATE cart')
            # mysql.connection.commit()
            # cursor.close()
    elif request.method == 'GET':
        msg = ''
        return render_template('checkout.html', total=total, msg=msg)
    else:
        msg = 'Please fill all boxes !'
        return render_template('checkout.html', total=total, msg=msg)


@app.route('/placeorder')
def placeorder():
    # cursor = mysql.connection.cursor()
    # cursor.execute('TRUNCATE cart')
    # mysql.connection.commit()
    # cursor.close()
    datas = dbcart.query.order_by(dbcart.name).all()
    for data in datas:
        db.session.delete(data)
    db.session.commit()
    return render_template('index.html')


@app.route('/items')
def items():
    data = dbitems.query.order_by(dbitems.name).all()
    return render_template('adminitems.html', items=data)


@app.route('/search/<name>')
def search(name):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE name = %s', (name,))
    # data = cursor.fetchall()
    # cursor.close()
    data = dbitems.query.filter_by(name=name).all()
    return render_template('items.html', items=data)


@app.route('/men')
def men():
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "men"')
    # data = cursor.fetchall()
    # cursor.close()
    data = dbitems.query.filter_by(category='men').all()
    return render_template('items.html', items=data, category='men')


@app.route('/men/<types>')
def mensort(types):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "men" and type = %s', (types,))
    # data = cursor.fetchall()
    # cursor.close()
    data = dbitems.query.filter_by(category='men').filter_by(types=types).all()
    return render_template('items.html', items=data, category='men')


@app.route('/men/price/<int:price>')
def menpricesort(price):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "men" and `discounted price` < %s', (price,))
    # data = cursor.fetchall()
    # cursor.close()
    _temp = dbitems.query.filter_by(category='men').all()
    data = []
    for i in _temp:
        if i.discounted_price <= price:
            data.append(i)
    return render_template('items.html', items=data, category='men')


@app.route('/women')
def women():
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "women"')
    # data = cursor.fetchall()
    # cursor.close()
    data = dbitems.query.filter_by(category='women').all()
    return render_template('items.html', items=data, category='women')


@app.route('/women/<types>')
def womensort(types):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "women" and type = %s', (types,))
    # data = cursor.fetchall()
    # cursor.close()
    data = dbitems.query.filter_by(
        category='women').filter_by(types=types).all()
    return render_template('items.html', items=data, category='women')


@app.route('/women/price/<int:price>')
def womenpricesort(price):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "women" and `discounted price` < %s', (price,))
    # data = cursor.fetchall()
    # cursor.close()
    _temp = dbitems.query.filter_by(category='women').all()
    data = []
    for i in _temp:
        if i.discounted_price <= price:
            data.append(i)
    return render_template('items.html', items=data, category='women')


@app.route('/child')
def child():
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "child"')
    # data = cursor.fetchall()
    # cursor.close()
    data = dbitems.query.filter_by(category='child').all()
    return render_template('items.html', items=data)


@app.route('/child/<types>')
def childsort(types):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "child" and type = %s', (types,))
    # data = cursor.fetchall()
    # cursor.close()
    data = dbitems.query.filter_by(
        category='child').filter_by(types=types).all()
    return render_template('items.html', items=data, category='child')


@app.route('/child/price/<int:price>')
def childpricesort(price):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM items WHERE category = "child" and `discounted price` < %s', (price,))
    # data = cursor.fetchall()
    # cursor.close()
    _temp = dbitems.query.filter_by(category='child').all()
    data = []
    for i in _temp:
        if i.discounted_price <= price:
            data.append(i)
    return render_template('items.html', items=data, category='child')


@app.route('/logout')
def logout():
    session['username'] = None
    session['id'] = None
    session['loggedin'] = False
    return redirect(url_for('login'))


@app.route('/logoutconfirmation')
def logoutconfirmation():
    return render_template('logout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        _username = request.form['username']
        _password = request.form['password']
        if _username == 'admin' and _password == 'admin':
            return render_template('adminfront.html')
        else:
            # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute(
            #     'SELECT * FROM account WHERE username = % s AND password = % s', (username, password, ))
            # account = cursor.fetchone()
            _account = dbaccount.query.filter_by(username=_username).first()
            if _account:
                session['loggedin'] = True
                session['id'] = _account.id
                session['username'] = _account.username
                msg = 'Logged in successfully !'
                return render_template('index.html')
            else:
                msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        _username = request.form['username']
        _password = request.form['password']
        _email = request.form['email']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute(
        #     'SELECT * FROM account WHERE username = % s', (username, ))
        # account = cursor.fetchone()
        _account = dbaccount.query.filter_by(username=_username).first()
        if _account:
            msg = 'Account already exists !'
        elif not _username or not _password or not _email:
            msg = 'Please fill out the form !'
        else:
            # cursor.execute(
            #     'INSERT INTO account VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            # mysql.connection.commit()
            try:
                new_user = dbaccount(username=_username,
                                     password=_password,
                                     email=_email)
                db.session.add(new_user)
                db.session.commit()
                msg = 'You have successfully registered !'
            except:
                msg = 'There was an error'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)

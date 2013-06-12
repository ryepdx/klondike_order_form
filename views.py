import bitcoinrpc
import prices
from app import app, db
from flask import abort, render_template, redirect, url_for
from forms import OrderForm
from models import Order, GroupBuy

@app.route('/', methods=['GET', 'POST'])
def show_form():
    form = OrderForm()

    if form.validate_on_submit():
        bitcoin = bitcoinrpc.connect_to_local()
        order = Order().populate_from_order_form(form)
        order.address = bitcoin.getnewaddress()
        db.session.add(order)
        
        for gb_form in form.group_buys:
            db.session.add(GroupBuy(order = order
                ).populate_from_groupbuy_form(gb_form))
        
        db.session.commit()
        
        return redirect(url_for(".order_completed", address = order.address))
    
    return render_template("index.html",
        form = form, prices = prices, site_name = app.config["SITE_NAME"])
    
@app.route('/<address>', methods=['GET'])
def order_completed(address):
    order = Order.query.filter_by(address = address).first_or_404()
    payment = (prices.K1 * order.k1s) + (prices.K16 * order.k16s) + (
        prices.K64 * order.k64s)
        
    if (payment == int(payment)):
        payment = int(payment)
    
    return render_template("completed.html",
        address = order.address, payment = payment,
        site_name = app.config["SITE_NAME"])

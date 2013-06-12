from app import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    k1s = db.Column(db.Integer, nullable=False, default=0)
    k16s = db.Column(db.Integer, nullable=False, default=0)
    k64s = db.Column(db.Integer, nullable=False, default=0)
    address = db.Column(db.String, nullable=False)
    refund_address = db.Column(db.String, nullable=False)
    k16substitution = db.Column(db.Boolean, nullable=False)
    bump = db.Column(db.Boolean, nullable=False)

    def __init__(self, username=None, email=None, k1s=0, k16s=0,
    k64s=0, address=None, refund_address=None, k16substitution=None,
    bump=None):
        self.username = username
        self.email = email
        self.k1s = k1s
        self.k16s = k16s
        self.k64s = k64s
        self.address = address
        self.refund_address = refund_address
        self.k16substitution = k16substitution
        self.bump = bump

    def __repr__(self):
        return '<Order #%s (for %s)>' % (self.id, self.username)
        
    def populate_from_order_form(self, order_form):
        self.username = order_form.information.username.data
        self.email = order_form.information.email.data
        self.refund_address = order_form.information.refund_address.data
        self.k1s = order_form.miners.k1s.data
        self.k16s = order_form.miners.k16s.data
        self.k64s = order_form.miners.k64s.data
        self.k16substitution = order_form.miners.k16substitution.data
        self.bump = order_form.miners.bump.data

        return self


class GroupBuy(db.Model):
    __tablename__ = 'groupbuys'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Order", backref = db.backref(
        'groupbuys', lazy = 'dynamic'))
    organizer = db.Column(db.String, nullable=False)
    batch = db.Column(db.Integer, nullable=False, default=1)
    chips = db.Column(db.Integer, nullable=False)
    
    def __init__(self, order = None, organizer=None, batch=None, chips=None):
        self.order = order
        self.organizer = organizer
        self.batch = batch
        self.chips = chips
        
    def __repr__(self):
        return '<GroupBuy by %s, batch %s, %s chips>' % (
            self.organizer, self.batch, self.chips)

    def populate_from_groupbuy_form(self, form):
        self.organizer = form.organizer.data
        self.batch = form.batch.data
        self.chips = form.chips.data
        
        return self

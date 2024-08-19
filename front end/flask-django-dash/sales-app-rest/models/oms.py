from app import db


class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date)
    order_customer_id = db.Column(db.Integer)
    order_status = db.Column(db.String(50))

    def __repr__(self):
        return (
            f"Order(order_id={self.order_id}, order_date={self.order_date}, "
            f"order_customer_id={self.order_customer_id}, order_status={self.order_status})"
        )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_item_order_id = db.Column(db.Integer, nullable=False)
    order_item_product_id = db.Column(db.Integer, nullable=False)
    order_item_quantity = db.Column(db.Integer, nullable=False)
    order_item_subtotal = db.Column(db.Float, nullable=False)
    order_item_product_price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return (
            f"OrderItem(order_item_id={self.order_item_id}, order_item_order_id={self.order_item_order_id}, "
            f"order_item_product_id={self.order_item_product_id}, order_item_quantity={self.order_item_quantity}, "
            f"order_item_subtotal={self.order_item_subtotal}, order_item_product_price={self.order_item_product_price})"
        )

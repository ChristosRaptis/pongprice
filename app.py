from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"
    url = db.Column(db.String(255), primary_key=True)
    product_name = db.Column(db.String(255))
    product_price_in_euros = db.Column(db.String(255))


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:7530@127.0.0.1/postgres"

    db.init_app(app)

    app.register_blueprint(main)

    return app


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    if q:
        results = (
            Product.query.filter(Product.product_name.match(q))
            .order_by(Product.product_price.asc())
            .all()
        )
    else:
        results = []

    return render_template("search_results.html", results=results)

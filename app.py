from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD


db = SQLAlchemy()

=======

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"
    url = db.Column(db.String(255), primary_key=True)
    product_name = db.Column(db.String(255))
    product_price = db.Column(db.String(255))

>>>>>>> 7ba69f6 (attempting to scrape Krefel)

def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:7530@127.0.0.1/postgres"
    db.init_app(app)
    app.register_blueprint(main)
    return app


main = Blueprint("main", __name__)

# define TSVECTOR type
TSVECTOR = db.Text().with_variant(db.Text(), "postgresql")


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    # Add a tsvector column for product_name
    product_name_tsvector = db.Column(TSVECTOR)

    # Define a hybrid property to generate the tsvector
    @hybrid_property
    def product_name_tsvector_expression(self):
        return func.to_tsvector("english", self.product_name)

    # Define a query expression to search the tsvector
    @classmethod
    @main.route("/search")
    def search(cls, query):
        search_vector = func.to_tsquery("english", query)
        results = cls.query.filter(cls.product_name_tsvector.match(search_vector)).all()
        return render_template("search_results.html", results=results)


@main.route("/")
def index():
    return render_template("index.html")
<<<<<<< HEAD
=======


@main.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    if q:
        
        results = Product.query.filter(Product.product_name.match(q))\
            .order_by(Product.product_price.asc()).all()
    else:
        results = []

    return render_template("search_results.html", results=results)
>>>>>>> 7ba69f6 (attempting to scrape Krefel)

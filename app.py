from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
class Product(db.Model):
    __tablename__ = "products"
    url = db.Column(db.String(255), primary_key=True)
    product_name = db.Column(db.String(255))
    product_price = db.Column(db.String(255))


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

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

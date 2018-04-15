import flask
from flask import request, send_from_directory
from products import Product

app = flask.Flask("Store", static_url_path='')


@app.route("/")
def index():
    products = Product.select()
    return flask.render_template("index.html",
                                 products=products)


@app.route("/products", methods=["GET", "POST"])
def show_products():
    if request.method == "POST":
        print(request.form)
        # todo: надо убедиться, что в форме корректные данные
        # validation
        product = Product(name=request.form['name'],
                          category=request.form['category'],
                          price=float(request.form['price']),
                          quantity=int(request.form['quantity']))
        product.save()

        return flask.redirect("/", code=404)
    else:
        return "<h1>Products page</h1>"

@app.route("/products/<int:id>", methods=["GET", "DELETE"])
def show_product(id):
    try:
        product = Product(id=id)
    except Exception:
        return "<h1>Not found</h1>", 404

    if request.method == "DELETE":
        product.delete()
        return "Deleted"

    return flask.render_template("product.html",
                                 product=product)

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

app.run("127.0.0.1", 9990, debug=True)

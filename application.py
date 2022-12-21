from productDAO import productDAO
from customerDAO import customerDAO
from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__, static_url_path='', static_folder='templates')

@app.route('/')
def index():
    return render_template('interface.html')

#*****************************************
@app.route('/customers', methods=['GET'])
def getAllCustmers():
    customers = customerDAO.getAll()
    return jsonify(customers)

#*****************************************
@app.route('/customers/<id>', methods=['GET'])
def getCustomerById(id):
    if len(id) == 0:
        return jsonify({}) , 204
    customer = customerDAO.findById(id)
    return jsonify(customer)

#*****************************************
@app.route('/customers/<id>', methods=['PUT'])
def update(id):

    customer = request.get_json()
    if len(customer) == 0:
        return jsonify({}), 404
    sqlData = (customer["cash"], customer["email"])
    customerDAO.updateCash(sqlData)
    return jsonify(customer)
   
#*****************************************
@app.route('/customers', methods=['POST'])
def createCustomer():
    customer = request.get_json()
    if not request.json:
        abort(400)
    else:
        sqlData = (customer["email"], customer["pass"], customer["cash"])
        customerDAO.create(sqlData)
        return jsonify({"done":True}) 

#*****************************************
@app.route('/customers/<id>', methods=['DELETE'])
def deleteCustomer(id):
    if "@" not in id:
        return jsonify({}), 404
    customerDAO.delete(id)
    return jsonify({"done":True})   

#*****************************************
@app.route('/shop', methods=['GET'])
def getAllProducts():
    products = productDAO.getAll()
    return jsonify(products)


@app.route('/shop/<id>', methods=['PUT'])
def updateProductById(id):
    product = request.get_json()
    if len(id) == 0:
        print("len is 0")
        return jsonify({}), 404
    sqlData = (product["qty"], product["id"])
    print(sqlData)
    productDAO.updateQuantity(sqlData)
    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)
from productDAO import productDAO
from customerDAO import customerDAO
from flask import Flask, session, url_for, redirect, abort, render_template, request, jsonify

app = Flask(__name__, static_url_path='', static_folder='templates')
app.secret_key = 'someSecrtetasdrgsadfgsdfg3ko'

@app.route('/')
def home():
    if not 'username' in session:
        return redirect(url_for('login'))
    return redirect(url_for('products'))


@app.route('/Login')
def login():
    return render_template('Login.html')
 
 
@app.route('/logout')
def logout():
    session.pop('username',None)
    return jsonify({"canLogin":False}) 
    
    
@app.route('/Products')
def products():
    if not 'username' in session:
        abort(401)
    return render_template('Products.html')


@app.route('/customers', methods=['GET'])
def getAllCustmers():
    customers = customerDAO.getAll()
    return jsonify(customers)


@app.route('/customers/<id>', methods=['GET'])
def getCustomerById(id):
    if len(id) == 0:
        return jsonify({}) , 204
    customer = customerDAO.findById(id)
    return jsonify(customer)


@app.route('/customers/<id>', methods=['PUT'])
def update(id):

    customer = request.get_json()
    if len(customer) == 0:
        return jsonify({}), 404
    sqlData = (customer["cash"], customer["email"])
    customerDAO.updateCash(sqlData)
    return jsonify(customer)
   

@app.route('/customers', methods=['POST'])
def createCustomer():
    customer = request.get_json()
    if not request.json:
        abort(400)
    else:
        sqlData = (customer["email"], customer["pass"], customer["cash"])
        customerDAO.create(sqlData)
        return jsonify({"createdUser":True}) 


@app.route('/customers/<id>', methods=['DELETE'])
def deleteCustomer(id):
    customers = customerDAO.getAll()
    for customer in customers:
        if customer['EMAIL'] == id:
            customerDAO.delete(id)
            return jsonify({"customerDeleted":True})  


@app.route('/processlogin/<id>/<password>', methods=['GET'])
def processLogin(id, password):

    if len(id) == 0:
        return jsonify({"canLogin":False}) 

    customer = customerDAO.findById(id)
    if not customer:
        return jsonify({"canLogin":False}) 

    else:
        db_email = customer[0]['EMAIL']
        db_pass = customer[0]['PASSWORD']

        if db_email == id and db_pass == password:
            session['username'] = db_email
            return jsonify({"canLogin":True}) 
        return jsonify({"canLogin":False}) 
        
        
@app.route('/shop', methods=['GET'])
def getAllProducts():
    products = productDAO.getAll()
    return jsonify(products)


@app.route('/shop/<id>', methods=['PUT'])
def updateProductById(id):
    product = request.get_json()
    if len(id) == 0:
        return jsonify({}), 404
    sqlData = (product["qty"], product["id"])
    productDAO.updateQuantity(sqlData)
    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)
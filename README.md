<h1 style="color: #001a79;">Data Representation Project</h1>
<hr style="border-top: 1px solid #001a79;" />


<h2 style="color: #001a79;">Description</h2> <br>
This Repository contains the files to run a Clothes Shop Web Application. The RESTful API uses flask and links to the customer and product tables of the shop database. The framework uses a login and products webpage to consume the API and perform CRUD operations on the shop data.

<br>

<h2 style="color: #001a79;">Contents of Repository</h2>

- **application.py** (RESTful API).
- **Login.html** (login web page).
- **Products.html** (products web page).
- **productDAO.py / customerDAO.py** (database access files).
- **loadData** folder (contains csv data for database).
- **requirements.txt** (details modules needed).


<h2 style="color: #001a79;">Running the Application</h2>

### On the Web: 
Go to the following link:
[http://moranc5.pythonanywhere.com/Login](http://moranc5.pythonanywhere.com/Login)



### Locally:
1. Locally host server on your computer (I used XXAMP,
[Download here](https://www.apachefriends.org/download.html)). 
2. Open XXAMP control panel and start MySQL and Apache. Once these services are running you can view your databases at the following [link](http://localhost/phpmyadmin/).
3. Run customerDAO.py and productDAO.py files to create shop database with customer and products table.<br>
Note that the files will only create the database / tables if they do not already exist.
4. Run application.py from command line to start flask server.
5. Copy local host url from command line and paste into browser.
6. Enter login details to start shopping.

<br>

<h2 style="color: #001a79;">Testing Aid:</h2>

**Note**:<br>
**The API tracks sessions, so you can wont have to login again if you have a live session on the server.** <br>
**All user entries have validation where they inform the user if the action has be completed.**


- username details:
    - email: newUser@shophere.com
    - password: datarep 

- Register New User:
- Login New User:
- Start Shopping 
    - Add Cash (Add Cash Button).
    - Alter order Quantity of product by clicking less and greater than symbols.
    - Purchase the stated order quantity for a given product via the Buy button (per row).
    - Logout.
- Delete New User:


Extra:
- The Login page has validation that will:
    - Prevent login with invalid username or password.
    - Prevent creation of new user if email already exists.
    - Alert you if trying to delete a user that doesn't exist.
- The Products page wont allow you to increase the order quantity past the current stock levels. <br>Also try and purchase something when you don't have enough money to see what happens!
    

<br>

<h2 style="color: #001a79;">Some of the CRUD Methods Used:</h2>

| Action      | Method | Function Name     |
| :---        |    :----:   |          ---: |
| Get all      | GET       | getAllProducts()    |
| Get all   | GET        | getAllCustomers()       |
| Find by id   | GET        | getCustomerById(id)      |
| Update   | PUT        | updateCustomerCash(customer)      |
| Update   | PUT        | updateProductQty(productTransaction)      |
| Create   | POST        | createCustomer(customer)     |
| Delete   | DELETE        | deleteUserReq(id)       |
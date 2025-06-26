from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session

from datetime import datetime

from database import get_user_orders, insert_order_ratings, add_item_to_cart, find_admin, get_store_info, insert_into_inventory, insert_supplier, insert_da, inventory_item, supplier, delivery, update_inventory, update_supplier, update_da, delete_inventory, delete_supplier, delete_da, authenticate_user, add_new_user, view_items_from_inventory,get_customer_details, getReviewData, exec_query, get_money, update_balance, get_items, update_quantity, update_order, get_customer_cart, update_customer_cart, update_user_profile

app = Flask(__name__)
app.secret_key = "secret_key_GroceryShop"

image_paths = {
  "Bananas": "/base/images/itemImg/Bananas.png",
  "Broccoli": "/base/images/itemImg/Broccolli.png",
  "Carrot-Red": "/base/images/itemImg/Carrot-Red.png",
  "Johnsons Hair oil": "/base/images/itemImg/Johnsons_oil.png",
  "Kashmir Apples": "/base/images/itemImg/Kashmir Apples.png",
  "Kiwis":"/base/images/itemImg/kiwi.png",
  "Loreal Paris Shampoo": "/base/images/itemImg/LP_shampoo.png",
  "Mama Earth Anti Hair fall Conditioner":"/base/images/itemImg/ME_conditioner.png",
  "Mama Earth Anti Hair fall Shampoo":"/base/images/itemImg/ME_shampoo.png",
  "Classmate Notebook": "/base/images/itemImg/notebook.png",
  "Valencia Oranges": "/base/images/itemImg/oranges.png",
  "Pear": "/base/images/itemImg/pear.png",
  "Nataraja Pencils": "/base/images/itemImg/pencil.png",
  "Rorito Ballpoint Pens": "/base/images/itemImg/pens.png",
  "Apsara Scale": "/base/images/itemImg/scale.png",
  "Dettol Hand Sanitizer": "/base/images/itemImg/sanitiser.png",
  "Colgate Whitening Toothpaste": "/base/images/itemImg/toothpaste.png",
  "Stayfree Sanitary Napkins": "/base/images/itemImg/sanitary_napkin.png",
  "Plastic Gala Broom": "/base/images/itemImg/Plastic Gala Broom.png",
  "Tomatoes": "/base/images/itemImg/tomato.png"
}

@app.route("/c/<CustomerID>")
def hello(CustomerID):
  return render_template('home.html', user_id = CustomerID)

@app.route("/loginpage", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['login-id']
        password = request.form['password']
        
        user = authenticate_user(username, password)

        if user:
            session['user'] = user
            return redirect(url_for('hello', CustomerID = user[0]))  
        else:
            error = 'Username or password is incorrect!'
            return render_template('loginpage.html', error=error)
    else:
        return render_template('loginpage.html')

@app.route("/registerpage", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        age = int(request.form['age'])
        phone_number = request.form['phone-number']
        login_id = request.form['login-id']
        password = request.form['password']
        address_line1 = request.form['address-line1']
        address_line2 = request.form['address-line2']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        pin_code = request.form['pin-code']

        add_new_user(first_name, last_name, age, phone_number, login_id, password, address_line1, address_line2, city, state, country, pin_code)
        return redirect(url_for('login'))
    else:
        return render_template('registerpage.html')
    
@app.route("/c/<CustomerID>/reviews")
def reviews(CustomerID):
   review, avg = getReviewData()
   return render_template('review_page.html', user_id = CustomerID, review = review, avg = avg)

@app.route("/c/<CustomerID>/reorder/<orderID>")
def reorder(CustomerID, orderID):
  add_item_to_cart(CustomerID,orderID)
  return redirect(url_for('view_cart',CustomerID=CustomerID))

@app.route("/c/<CustomerID>/cart", methods=["GET", "POST"])
def view_cart(CustomerID):
  customer = get_customer_details(CustomerID)
  if(customer):
    if request.method == "GET":
        item = get_items(CustomerID)
        cost = sum(i['Quantity'] * i['price'] for i in item)
        balance = exec_query(f'SELECT Balance from Wallet Where CustomerID={CustomerID}')
        balance = balance[0]['Balance']
        return render_template('checkout.html', item=item, cost=cost, tcost=cost + 10, user_id=CustomerID, images=image_paths,bal=balance)
    elif request.method == "POST":
        item_id = request.form.get("item_id")
        quantity = request.form.get("quantity")
        query = f'UPDATE Cart SET Quantity ={quantity} where Customer_ID={CustomerID} and Item_ID={item_id}'
        update_quantity(query)
        item = get_items(CustomerID)
        cost = sum(i['Quantity'] * i['price'] for i in item)
        total_cost = cost + 10
        return jsonify({
            "message": "Quantity updated successfully",
            "total_cost": total_cost,
            "cost": cost
        })
  else:
    return render_template('loginpage.html')
  

@app.route("/c/<CustomerID>/cart/pay",methods=["POST"])
def cart_final(CustomerID):
  temp = exec_query('0')
  cart_item = exec_query(f'Select Item_ID , Quantity from Cart where Customer_ID={CustomerID}')
  for i in cart_item:
    storeId = exec_query(f"select StoreID from Inventory where itemID = {i['Item_ID']}")
    storeId = storeId[0]['StoreID']
    res = update_order(f"UPDATE Inventory SET stock = stock - {i['Quantity']} where storeID = {storeId}", 1, i['Item_ID'])
    if res == 0:
       temp = exec_query(f'delete from cart where Customer_ID = {CustomerID}')
       return jsonify({'error': 'Transaction failed'}), 400
  payment_method = request.form['payment_method']
  total_cost = int(request.form['total_cost'])
  if(payment_method=='Wallet'):
     change = exec_query(f'Select Balance from Wallet where CustomerID = {CustomerID}')[0]['Balance'] - total_cost
     update_order(f'UPDATE Wallet SET Balance = {change} where CustomerID = {CustomerID}', 2, i['Item_ID'])
  cart_item = exec_query(f'Select Item_ID , Quantity from Cart where Customer_ID={CustomerID}')
  for i in cart_item:
     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     que = f"INSERT INTO Orders (CustomerID,AgentID,itemID,quantity,OrderStatus,ETA,OrderTime) VALUES ({CustomerID},1,{i['Item_ID']},{i['Quantity']},'Delivered',5,'{current_time}')"
     update_order(que, 3, i['Item_ID'])
  return 'Query executed successfully'


@app.route("/c/<CustomerID>/orders")
def order_page(CustomerID):
  orders = get_user_orders(CustomerID)
  return render_template('order_page.html', orders = orders, images = image_paths, user_id = CustomerID)

@app.route("/c/<CustomerID>/orders/<orderID>/rate")
def take_rating(CustomerID, orderID):
  return render_template('review.html', userid = CustomerID, orderid = orderID)

@app.route("/c/<CustomerID>/orders/<orderID>/ratings", methods = ['post'])
def ratings_to_db(CustomerID, orderID):
  data = request.form
  insert_order_ratings(orderID,data['rating'],data['opinion'])
  flash('Feedback submitted successfully', 'success')
  return redirect(url_for('order_page',CustomerID = CustomerID))

@app.route("/a")
def admin():
  return render_template('admin_login.html')

@app.route("/a/login", methods = ['post'])
def check_admin():
  data = request.form
  result, adminID = find_admin(data['first'], data['password'])
  if result:
    return redirect(url_for('admin_home', AdminID = adminID))
  else:
    flash('Incorrect login credentials', 'error')
    return redirect(url_for('admin'))

@app.route("/a/<AdminID>")
def admin_home(AdminID):
  store_info = get_store_info(AdminID)
  return render_template('admin_main.html', admin = AdminID,store = store_info)

@app.route("/a/<AdminID>/modify")
def modify_page(AdminID):
  return render_template('modify_db.html', admin = AdminID)

@app.route("/a/<AdminID>/stats")
def database_stats(AdminID):
    query1 = 'SELECT itemID, SUM(quantity) AS total_quantity FROM Orders GROUP BY itemID ORDER BY total_quantity DESC LIMIT 1;'
    query2 = 'SELECT itemID FROM Inventory WHERE stock < 10;'
    query3 = 'SELECT * FROM DeliveryAgent;'
    query4 = 'SELECT * FROM Inventory;'
    return render_template('db_stats.html',admin=AdminID,tab1=exec_query(query1),tab2=exec_query(query2),tab3=exec_query(query3),tab4=exec_query(query4))

@app.route("/a/<AdminID>/query")
def query_page(AdminID):
   return render_template('query_page.html', admin = AdminID)

@app.route("/a/<AdminId>/query/execute", methods=['POST'])
def execute_query(AdminId):
    data = request.get_json()
    query = data['query']
    result = exec_query(query)
    return jsonify(result)

@app.route("/c/<CustomerID>/wallet",methods=['POST','GET'])
def view_wallet(CustomerID):
    if request.method == 'POST':
        amount = request.form.get('amount')
        if amount is not None and amount.isdigit():
            customer_id = int(CustomerID)
            amount = int(amount)
            update_balance(customer_id, amount)
            new_balance = get_money(customer_id)[0]['Balance']
            return jsonify({'bal': new_balance})
        else:
            return jsonify({'error': 'Invalid amount'}), 400  # Bad request
    bal = get_money(CustomerID)
    return render_template('wallet.html',bal=bal[0]['Balance'], user_id = CustomerID)

@app.route("/a/<AdminID>/insert")
def insert_db(AdminID):
  return render_template('insert_page.html', admin = AdminID)

@app.route("/a/<AdminID>/update")
def update_db(AdminID):
  return render_template('update_page.html', admin = AdminID)

@app.route("/a/<AdminID>/delete")
def delete_db(AdminID):
  return render_template('delete_page.html', admin = AdminID)

@app.route('/fetch_record', methods=['post'])
def fetch_record():
  option = request.json['option']
  record_id = request.json['recordID']
  admin = request.json['admin']
  if option == 'inventory':
    result = inventory_item(record_id)
  elif option == 'supplier':
    result = supplier(record_id)
  elif option == 'delivery':
    result = delivery(record_id, admin)
  return jsonify(result)
  
@app.route('/a/<AdminID>/updatedb', methods = ['post'])
def update_db_check(AdminID):
  submit_method = request.form.get('submit_method')
  data = request.form
  if submit_method == 'inventory':
    update_inventory(data)
    flash("Inventory updated", "success")
  elif submit_method == 'supplier':
    update_supplier(data)
    flash("Supplier details updated", "success")
  elif submit_method == 'delivery':
    update_da(data)
    flash("Delivery Agent details updated", "success")
  return redirect(url_for('update_db',AdminID = AdminID))

@app.route("/a/<AdminID>/inserttodb", methods=['post'])
def insert_to_db(AdminID):
  submit_method = request.form.get('submit_method')
  data = request.form
  if submit_method == 'inventory':
    insert_into_inventory(data, AdminID)
    flash("Item added to inventory", "success")
  elif submit_method == 'supplier':
    insert_supplier(data)
    flash("Supplier added to database", "success")
  elif submit_method == 'delivery':
    insert_da(data, AdminID)
    flash("Delivery Agent added to database", "success")
  return redirect(url_for('insert_db',AdminID = AdminID))

@app.route("/a/<AdminID>/deletedb", methods = ['post'])
def delete_from_db(AdminID):
  submit_method = request.form.get('submit_method')
  data = request.form
  if submit_method == 'inventory':
    delete_inventory(data['primarykey'])
    flash("Item deleted from inventory", "warning")
  elif submit_method == 'supplier':
    delete_supplier(data['primarykey'])
    flash("Supplier deleted from database", "warning")
  elif submit_method == 'delivery':
    delete_da(data['primarykey'])
    flash("Delivery Agent deleted from database", "warning")
  return redirect(url_for('delete_db',AdminID = AdminID))


@app.route('/c/<CustomerID>/Profile')
def profile(CustomerID):
    customer = get_customer_details(CustomerID)
    if customer:
        return render_template('user_profile.html', customer=customer, user_id= CustomerID)
    else:
        return render_template('loginpage.html')
    
@app.route('/c/<CustomerID>/edit')
def edit_profile(CustomerID):
  customer = get_customer_details(CustomerID)
  return render_template('edit_profile.html', customer=customer, user_id= CustomerID)

@app.route('/<CustomerID>/edit', methods = ['post'])
def update_profile(CustomerID):
   data = request.form
  #  return data
   update_user_profile(data, CustomerID)
   flash('Profile updated successfully','success')
   return redirect(url_for('profile',CustomerID = CustomerID))

@app.route("/c/<CustomerID>/Products", methods=['GET', 'POST'])
def view_products(CustomerID):
    category_filter = request.args.get('category')
    sort_by = request.args.get('sort')

    products = view_items_from_inventory(category_filter, sort_by)

    for product in products:
        if product['ItemName'] in image_paths:
            product['image'] = image_paths[product['ItemName']]
        else:
            product['image'] = "/base/images/placeholder.jpg"
    cart_info = get_customer_cart(CustomerID)
    return render_template('Products.html', products=products, user_id=CustomerID, cart = cart_info)

@app.route('/c/<CustomerID>/about us')
def about_us(CustomerID):
  return render_template('about_us_page.html', user_id= CustomerID)

@app.route("/c/<CustomerID>/privacy policy")
def privacy_policy(CustomerID):
  return render_template('privacy_policy.html', user_id= CustomerID)

@app.route('/update_cart_quantity', methods=['POST'])
def update_cart_quantity():
    data = request.json
    cart_id = data['cart_id']
    item_id = data['item_id']
    quantity = data['quantity']
    operation = data['op']
    update_customer_cart(cart_id, item_id, quantity, operation)
    return jsonify({'message': 'Cart quantity updated successfully'})

@app.route("/")
def landing_page():
  return render_template('main.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

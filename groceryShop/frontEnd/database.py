import mysql.connector as ps
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DB_USERNAME")
pwd = os.getenv("DB_PASSWORD")
database = os.getenv("DB_DATABASE")
host = os.getenv("DB_HOST")

mycon = ps.connect(
    user=username,
    host=host,
    password=pwd,
    database=database
)

def get_user_orders(userID):
    query = '''select o.customerID, o.OrderID, o.itemID, i.ItemName, i.price, i.unit, o.quantity, o.quantity * i.price as cost, 
    o.OrderTime, o.OrderStatus from orders o join inventory i on o.itemID = i.itemID 
    where CustomerID = {} group by o.OrderID, i.ItemName, i.price, i.unit order by OrderTime desc'''.format(userID)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchall()
    return result

def insert_order_ratings(orderID,stars,description):
    query = '''INSERT INTO reviews VALUES (%s, %s, %s)'''
    values = (orderID, stars, description)
    cur = mycon.cursor()
    cur.execute(query, values)
    mycon.commit()

def add_item_to_cart(customerID, orderID):
    query = '''select itemID, quantity from orders where orderID = {}'''.format(orderID)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    items = cur.fetchall()
    for item in items:
        itemID = item['itemID']
        quantity = item['quantity']
        query_check = "select * from cart where Customer_ID = {} and Item_ID = {}".format(customerID,itemID)
        cur.execute(query_check)
        result = cur.fetchall()
        if result:
            query_add = '''update cart set quantity = quantity + {} where Customer_ID = {}'''.format(quantity,customerID)
            cur.execute(query_add)
        else:
            query = '''INSERT INTO cart VALUES (%s, %s, %s, %s)'''
            values = (customerID, customerID, itemID, quantity)
            cur.execute(query, values)
        mycon.commit()

def find_admin(adminID, password):
    query = "SELECT * FROM admin WHERE AdminID = %s AND admin_pwd = %s"
    cur = mycon.cursor(dictionary = True)
    cur.execute(query, (adminID, password))
    data = cur.fetchall()
    if data:
        return True, data[0]['AdminID']
    else:
        return False, None
    
def get_store_info(adminID):
    query = '''select StoreID from admin where AdminID = {}'''.format(adminID)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchall()[0]
    query = '''select * from offline_stores where storeID = {}'''.format(result['StoreID'])
    cur.execute(query)
    data = cur.fetchall()[0]
    return data

def insert_into_inventory(data, admin):
    query = "select StoreID from admin where AdminID = {}".format(admin)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    store = cur.fetchall()[0]['StoreID']
    itemName = data['itemName']
    category = data['category']
    price = data['price']
    unit = data['unit']
    stock = data['stock']
    description = data['itemDescription']
    query = '''INSERT INTO inventory (StoreID, ItemName, Unit, price, stock, category, itemDescription) 
           VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    cur.execute(query, (store, itemName, unit, price, stock, category, description))
    mycon.commit()

def insert_supplier(data):
    name = data['supplierName']
    category = data['category']
    add1 = data['AddressLine1']
    add2 = data['AddressLine2']
    city = data['city']
    state = data['state']
    country = data['country']
    pin = data['pincode']
    query = '''insert into supplier(Name, Category, AddressLine1, AddressLine2, City, State, Country, PIN_code) 
    values(%s,%s,%s,%s,%s,%s,%s,%s)'''
    cur = mycon.cursor(dictionary=True)
    cur.execute(query,(name,category,add1,add2,city,state,country,pin))
    mycon.commit()

def insert_da(data, admin):
    query = "select StoreID from admin where AdminID = {}".format(admin)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    store = cur.fetchall()[0]['StoreID']
    name = data['agentname']
    p_no = data['phonenumber']
    query = '''insert into deliveryagent(AgentName, PhoneNumber, StoreID) values(%s,%s,%s)'''
    cur.execute(query,(name,p_no,store))
    mycon.commit()

def inventory_item(recordID):
    query = '''select * from inventory where itemID = {}'''.format(recordID)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchall()
    if not result:
        return None
    return result[0]

def supplier(recordID):
    query = '''select * from supplier where Supplier_ID = {}'''.format(recordID)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchall()
    if not result:
        return None
    return result[0]

def delivery(recordID, admin):
    query = '''select StoreID from admin where AdminID = {}'''.format(admin)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    store = cur.fetchall()[0]['StoreID']
    query = '''select * from deliveryagent where AgentID = %s and StoreID = %s'''
    cur.execute(query, (recordID, store))
    result = cur.fetchall()
    if not result:
        return None
    return result[0]

def update_inventory(data):
    itemID = data['primarykey']
    name = data['itemName']
    unit = data['unit']
    price = data['price']
    stock = data['stock']
    cat = data['category']
    desc = data['itemDescription']
    query = '''update inventory
    set ItemName = %s, Unit = %s, price = %s, category = %s, stock = %s, itemDescription = %s
    where itemID = %s'''
    cur = mycon.cursor(dictionary=True)
    cur.execute(query,(name,unit,price,cat,stock,desc,itemID))
    mycon.commit()

def update_supplier(data):
    s_id = data['primarykey']
    name = data['supplierName']
    cat = data['category']
    add1 = data['AddressLine1']
    add2 = data['AddressLine2']
    city = data['city']
    state = data['state']
    country = data['country']
    pin = data['pincode']
    query = '''update supplier
    set Name = %s, Category = %s, AddressLine1 = %s, AddressLine2 = %s, City = %s, State = %s, Country = %s, PIN_code = %s
    where Supplier_ID = %s'''
    cur = mycon.cursor(dictionary=True)
    cur.execute(query,(name,cat,add1,add2,city,state,country,pin,s_id))
    mycon.commit()

def update_da(data):
    d_id = data['primarykey']
    name = data['agentname']
    phone = data['phonenumber']
    query = '''update deliveryagent
    set AgentName = %s, PhoneNumber = %s
    where AgentID = %s'''
    cur = mycon.cursor(dictionary=True)
    cur.execute(query,(name,phone,d_id))
    mycon.commit()

def delete_inventory(p_id):
    query = '''delete from inventory
    where itemID = {}'''.format(p_id)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    mycon.commit()

def delete_supplier(p_id):
    query = '''delete from supplier
    where Supplier_ID = {}'''.format(p_id)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    mycon.commit()

def delete_da(p_id):
    query = '''delete from deliveryagent
    where AgentID = {}'''.format(p_id)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    mycon.commit()


def view_items_from_inventory(category_filter=None, sort_by=None):
    query = "SELECT * FROM Inventory where stock > 0"

    if category_filter:
        query += " AND Category = '{}'".format(category_filter)

    if sort_by:
        if sort_by == 'price-asc':
            query += " ORDER BY price ASC"
        elif sort_by == 'price-desc':
            query += " ORDER BY price DESC"
        elif sort_by == 'name-asc':
            query += " ORDER BY ItemName ASC"
        elif sort_by == 'name-desc':
            query += " ORDER BY ItemName DESC"

    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchall()
    return result


def authenticate_user(username, password):
    query = "SELECT * FROM Customers WHERE LoginID = %s AND Customer_Password = %s"
    cur = mycon.cursor()
    cur.execute(query, (username, password))
    user = cur.fetchone()
    return user

def add_new_user(first_name, last_name, age, phone_number, login_id, password, address_line1, address_line2, city, state, country, pin_code):
    query = '''INSERT INTO Customers (FirstName, LastName, Age, PhoneNumber, LoginID, Customer_Password, AddressLine1, AddressLine2, City, State, Country, pin_code) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    values = (first_name, last_name, age, phone_number, login_id, password, address_line1, address_line2, city, state, country, pin_code)
    cur = mycon.cursor()
    cur.execute(query, values)
    mycon.commit()

def getReviewData():
    query = "select * from reviews"
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    reviews = cur.fetchall()
    result = []
    total = 0
    total_stars = 0
    for review in reviews:
        total += 1
        orderID = review['OrderID']
        query = "select CustomerID from orders where OrderID = {}".format(orderID)
        cur.execute(query)
        custID = cur.fetchall()[0]['CustomerID']
        query = '''select FirstName, LastName, LoginID from customers where CustomerID = {}'''.format(custID)
        cur.execute(query)
        l = cur.fetchall()[0]
        details = {}
        details['first_name'] = l['FirstName']
        details['last_name'] = l['LastName']
        details['id'] = l['LoginID']
        details['stars'] = review['stars']
        total_stars += details['stars']
        details['non_stars'] = 5 - details['stars']
        details['comment'] = review['description']
        result.append(details)
    avg_stars = round(total_stars / total, 2)
    return result, avg_stars

def exec_query(query):
    cur= mycon.cursor(dictionary=True)
    if query == '0':
        cur.execute("START TRANSACTION")
        return ''
    que = query
    cur.execute(que)
    result = cur.fetchall()
    return result

def update_quantity(que):
    cur = mycon.cursor()
    cur.execute(que)
    mycon.commit()

def get_money(CustomerID):
    mycursor = mycon.cursor(dictionary=True)
    mycursor.execute(f'Select Balance from Wallet where CustomerID = {CustomerID}')
    res = mycursor.fetchall()
    return res


def update_balance(customer_id, amount):
    cursor = mycon.cursor()
    query = f'UPDATE wallet SET Balance = Balance + {amount} WHERE CustomerID = {customer_id}'
    cursor.execute(query)
    mycon.commit()

def get_items(CustomerID):
    mycursor = mycon.cursor(dictionary=True)
    mycursor.execute(f'SELECT Item_ID,Quantity FROM Cart Where Customer_ID = {CustomerID}')
    item = mycursor.fetchall()
    mycursor.execute(f'select itemID,ItemName, price , stock from Inventory where itemId IN (select Item_ID from Cart where Customer_ID = {CustomerID})')
    item_detail = mycursor.fetchall()
    for i in range(len(item)):
        item_detail[i]['Quantity'] = item[i]['Quantity']
    return item_detail

def update_order(Query, mode, itemID):
    mycursor = mycon.cursor(dictionary=True)
    mycursor.execute(Query)

    if mode == 1:
        query = "SELECT stock FROM inventory WHERE itemID = %s"
        mycursor.execute(query, (itemID,))
        result = mycursor.fetchone()
        stock = result['stock']
        if stock < 0:
            print("Stock negative")
            mycon.rollback()
            return 0
    mycon.commit()
    if mode == 1:
        return 1

def get_user_orders(userID, category=None, sort=None):
    query = '''select o.customerID, o.OrderID, o.itemID, i.ItemName, i.price, i.unit, o.quantity, o.quantity * i.price as cost, 
    o.OrderTime, o.OrderStatus from orders o join inventory i on o.itemID = i.itemID 
    where CustomerID = {}'''.format(userID)

    if category:
        query += " AND i.category = '{}'".format(category)

    if sort:
        if sort == 'price-asc':
            query += " ORDER BY i.price ASC"
        elif sort == 'price-desc':
            query += " ORDER BY i.price DESC"
        elif sort == 'name-asc':
            query += " ORDER BY i.ItemName ASC"
        elif sort == 'name-desc':
            query += " ORDER BY i.ItemName DESC"

    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchall()
    return result

def get_customer_details(CustomerID):
    query = "SELECT * FROM Customers WHERE CustomerID = %s"
    cursor = mycon.cursor(dictionary=True)
    cursor.execute(query, (CustomerID,))
    result = cursor.fetchone()
    return result

def get_customer_cart(customerID):
    query = "select Item_ID, Quantity from cart where Customer_ID = {}".format(customerID)
    cur = mycon.cursor(dictionary=True)
    cur.execute(query)
    cart = cur.fetchall()
    cart_item = {}
    for i in cart:
        cart_item[i['Item_ID']] = i['Quantity']
    query = "select itemID, ItemName from inventory"
    cur.execute(query)
    inventory = cur.fetchall()
    cart_info = {}
    for item in inventory:
        if item['itemID'] in cart_item:
            cart_info[item['ItemName']] = cart_item[item['itemID']]
        else:
            cart_info[item['ItemName']] = 0
    return cart_info

def update_customer_cart(cartID, itemID, quantity, op):
    cur = mycon.cursor(dictionary=True)
    if op == 1:
        if quantity == 1:
            query = "INSERT INTO cart (Cart_ID, Customer_ID, Item_ID, Quantity) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (cartID, cartID, itemID, quantity))
        else:
            query = "UPDATE cart SET Quantity = %s WHERE Cart_ID = %s AND Customer_ID = %s AND Item_ID = %s"
            cur.execute(query, (quantity, cartID, cartID, itemID))
        mycon.commit()
    elif op == 2:
        if quantity == 0:
            query = "DELETE from cart where Cart_ID = %s AND Customer_ID = %s AND Item_ID = %s"
            cur.execute(query, (cartID, cartID, itemID))
        else:
            query = "UPDATE cart SET Quantity = %s WHERE Cart_ID = %s AND Customer_ID = %s AND Item_ID = %s"
            cur.execute(query, (quantity, cartID, cartID, itemID))
        mycon.commit()

def update_user_profile(data, CustomerID):
    fname = data['customerName'].split()[0]
    lname = data['customerName'].split()[1]
    age = data['age']
    phone = data['phoneNumber']
    email = data['email']
    add1 = data['addressline1']
    add2 = data['addressline2']
    city = data['city']
    state = data['state']
    pin = data['pincode']
    query = '''update customers
    set FirstName = %s, LastName = %s, LoginID = %s, AddressLine1 = %s, AddressLine2 = %s, City = %s,
    State = %s, pin_code = %s, Age = %s, PhoneNumber = %s
    where CustomerID = %s'''
    cur = mycon.cursor(dictionary=True)
    cur.execute(query,(fname,lname,email,add1,add2,city,state,pin,age,phone, CustomerID))
    mycon.commit()
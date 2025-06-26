USE GroceryShop;

-- CONFLICTING TRANSACTIONS
-- When Two users buys at the same time
START TRANSACTION;
SELECT Quantity INTO @Cart_quantity from cart where Cart_ID = 1 and Item_ID = 1;
SELECT @Cart_quantity * price INTO @Cart_cost from inventory where itemID = 1;
UPDATE inventory SET stock = stock - @Cart_quantity where itemID = 1;
INSERT INTO Orders (CustomerID,AgentID,itemID,quantity,OrderStatus,ETA,OrderTime) VALUES (1,1,1,@Cart_quantity,'Delivered',5,NOW());
UPDATE wallet SET Balance = Balance - @Cart_cost where CustomerID = 1;
COMMIT;

START TRANSACTION;
SELECT Quantity INTO @Cart_quantity from cart where Cart_ID = 2 and Item_ID = 1;
SELECT @Cart_quantity * price INTO @Cart_cost from inventory where itemID = 1;
UPDATE inventory SET stock = stock - @Cart_quantity where itemID = 1;
INSERT INTO Orders (CustomerID,AgentID,itemID,quantity,OrderStatus,ETA,OrderTime) VALUES (2,1,1,@Cart_quantity,'Delivered',5,NOW());
UPDATE wallet SET Balance = Balance - @Cart_cost where CustomerID = 2;
COMMIT;

-- When admin updates the stock and user buys that item at the same time
START TRANSACTION;
UPDATE inventory SET stock = 100 WHERE itemID = 1;
COMMIT;

START TRANSACTION;
SELECT Quantity INTO @Cart_quantity from cart where Cart_ID = 1 and Item_ID = 1;
SELECT @Cart_quantity * price INTO @Cart_cost from inventory where itemID = 1;
UPDATE inventory SET stock = stock - @Cart_quantity where itemID = 1;
INSERT INTO Orders (CustomerID,AgentID,itemID,quantity,OrderStatus,ETA,OrderTime) VALUES (1,1,1,@Cart_quantity,'Delivered',5,NOW());
UPDATE wallet SET Balance = Balance - @Cart_cost where CustomerID = 1;
COMMIT;

-- NON CONFLICTING TRANSACTIONS

-- When two users update their wallet at the same time
START TRANSACTION;
UPDATE wallet SET Balance = Balance - 100 WHERE CustomerID = 1 and Balance > 0;
COMMIT;

START TRANSACTION;
UPDATE wallet SET Balance = Balance - 100 WHERE CustomerID = 2 and Balance > 0;
COMMIT;

-- When two users update their profile at the same time
START TRANSACTION;
UPDATE customers SET PhoneNumber = 9473829108 where CustomerID = 1;
COMMIT;

START TRANSACTION;
UPDATE customers SET PhoneNumber = 9473289108 where CustomerID = 2;
COMMIT;

-- Two admin viewing statistics at the same time
START TRANSACTION;
Select PhoneNumber into @AgentInfo from DeliveryAgent where AgentID = 1;
select @AgentInfo as Phonenumber;
COMMIT;

START TRANSACTION;
Select PhoneNumber into @AgentInfo from DeliveryAgent where AgentID = 1;
select @AgentInfo as Phonenumber;
COMMIT;

-- Two users registering at the same time
START TRANSACTION;
Select Customer_Password into @pass from Customers where CustomerID = 1;
select @pass as PasswordUser;
COMMIT;

START TRANSACTION;
Select Customer_Password into @pass from Customers where CustomerID = 2;
select @pass as PasswordUser;
COMMIT;

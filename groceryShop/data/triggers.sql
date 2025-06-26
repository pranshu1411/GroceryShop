USE GroceryShop;

-- Trigger to create a Customer's wallet when they create their account
DELIMITER //

CREATE TRIGGER add_wallet_trigger
AFTER INSERT ON Customers
FOR EACH ROW
BEGIN
    DECLARE new_upi_id VARCHAR(20);
    SET new_upi_id = CONCAT(NEW.PhoneNumber, '@paytm');

    INSERT INTO Wallet (CustomerID, Balance, UPI_ID)
    VALUES (NEW.CustomerID, 0, new_upi_id);
END;
//

DELIMITER ;

-- Trigger to delete a Customer's wallet if they delete their account
DELIMITER //

CREATE TRIGGER delete_wallet_trigger
AFTER DELETE ON Customers
FOR EACH ROW
BEGIN
    DELETE FROM Wallet WHERE CustomerID = OLD.CustomerID;
END;
//

DELIMITER ;

-- Trigger to delete the item from the cart when it has been ordered
DELIMITER //

CREATE TRIGGER delete_from_cart_trigger
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
    DELETE FROM Cart WHERE Customer_ID = NEW.CustomerID AND Item_ID = NEW.itemID;
END;
//

DELIMITER ;
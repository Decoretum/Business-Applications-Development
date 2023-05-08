CREATE DATABASE TAIWANSTEEL;
SHOW DATABASES;

USE TAIWANSTEEL;
SHOW TABLES;

desc Inventory_notifyparty;
desc Inventory_finalorder;
desc Inventory_orderedproduct;
desc Inventory_product;

SELECT * FROM Inventory_consignee;
SELECT * FROM Inventory_finalorder
where Finished = True;

SELECT Inventory_finalorder.id, Inventory_orderedproduct.OrderedProductID, Inventory_orderedproduct.totalcost
FROM Inventory_orderedproduct, Inventory_finalorder
WHERE Inventory_orderedproduct.OrderID_id = Inventory_finalorder.id
AND Inventory_finalorder.Finished = False;
#AND Inventory_finalorder.TotalCost >= 100;

SELECT * FROM Inventory_product;
SELECT * FROM auth_user;
SELECT * FROM auth_group;

UPDATE Inventory_product
SET Status = 1
WHERE Name = "Jedd's Steel";

UPDATE Inventory_product
SET Status = 1
WHERE Name = "Steel Sheets";

UPDATE Inventory_product
SET Stock = 0
WHERE Name = "Steel Sheets"
OR Name = "Jedd's Steel";

SELECT CONCAT(Inventory_notifyparty.id,": ", Name) AS 'PK and Address', Address
FROM Inventory_notifyparty, Inventory_finalorder
WHERE Inventory_notifyparty.id = Inventory_finalorder.notifyname_id
AND Inventory_finalorder.id <= 10;

SELECT CONCAT(Inventory_orderedproduct.id, ": ", Inventory_Product.Name) as 'OrderedProduct ID and Product Name', CONCAT('$', Inventory_orderedproduct.totalcost) as 'Total Cost' 
FROM Inventory_orderedproduct, Inventory_finalorder, Inventory_Product
WHERE Inventory_orderedproduct.orderid_id = Inventory_finalorder.id
AND Inventory_orderedproduct.marks_id = Inventory_product.id
AND Inventory_finalorder.id <= 10; 
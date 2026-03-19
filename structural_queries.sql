-- List orders and customers
SELECT o.OrderID, c.FullName, o.OrderDatetime, o.CurrentStatus FROM [Orders] o
JOIN [Customers] c ON o.CustomerID = c.CustomerID
WHERE o.CurrentStatus = 'paid'
ORDER BY o.OrderDatetime
Limit 10;

-- Bring products from each order
SELECT oi.OrderID, p.ProductName, oi.Quantity, oi.UnitPrice FROM [OrderItems] oi
JOIN [Products] p ON oi.ProductID = p.ProductID
ORDER BY oi.OrderID
Limit 10;
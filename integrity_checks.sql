-- Detect orders with non-existent CustomerID
SELECT * FROM [Orders] o
LEFT JOIN [Customers] c ON o.CustomerID = c.CustomerID
WHERE c.CustomerID IS NULL
LIMIT 10;

-- Detect products in OrderItems that do not exist
SELECT * FROM [OrderItems] oi
LEFT JOIN [Products] p ON oi.ProductID = p.ProductID
WHERE p.ProductID IS NULL
LIMIT 10;

-- Detect impossible states
SELECT * FROM [Orders]
WHERE CurrentStatus NOT IN ('created','paid','shipped','packed','delivered','cancelled')
LIMIT 10;
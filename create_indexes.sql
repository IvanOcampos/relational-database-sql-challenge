-- Indexes on foreign keys and critical columns
CREATE INDEX idx_orders_customer ON Orders(CustomerID);
CREATE INDEX idx_orderitems_order ON OrderItems(OrderID);
CREATE INDEX idx_orderitems_product ON OrderItems(ProductID);
CREATE INDEX idx_payments_order ON Payments(OrderID);
CREATE INDEX idx_orderstatushistory_order ON OrderStatusHistory(OrderID);
CREATE INDEX idx_orderaudit_order ON OrderAudit(OrderID);
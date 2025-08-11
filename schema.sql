DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL UNIQUE,
  verify NUMERIC NOT NULL DEFAULT 0,
  verify_code NUMERIC NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create table: Category
DROP TABLE IF EXISTS category;
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT,
    user_id INTEGER NOT NULL
);

-- Create table: Product
DROP TABLE IF EXISTS product;
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    cost DECIMAL(10, 2),
    price DECIMAL(10, 2),
    image TEXT,
    current_stock INTEGER DEFAULT 0,
    description TEXT,
    user_id INTEGER NOT NULL
);

-- Create table: "Order"
DROP TABLE IF EXISTS sale_order;
CREATE TABLE "sale_order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date_time DATETIME NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    paid DECIMAL(10, 2) DEFAULT 0,
    user_id INTEGER NOT NULL,
    remark TEXT
);

-- Create table: OrderItem
DROP TABLE IF EXISTS sale_order_item;
CREATE TABLE sale_order_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);


-- Insert sample data into Category
INSERT INTO category (name, image, user_id) VALUES
('Electronics', 'electronics.jpg', 1),
('Clothing', 'clothing.jpg', 1),
('Books', 'books.jpg', 1),
('Furniture', 'furniture.jpg', 1),
('Sports', 'sports.jpg', 1),
('Toys', 'toys.jpg', 1),
('Shoes', 'shoes.jpg', 1),
('Beauty', 'beauty.jpg', 1),
('Groceries', 'groceries.jpg', 1),
('Stationery', 'stationery.jpg', 1);

-- Insert sample data into Product
INSERT INTO product (name, category_id, cost, price, image, current_stock, description, user_id) VALUES
('Smartphone', 1, 300.00, 450.00, 'smartphone.jpg', 50, 'Latest smartphone model', 1),
('T-shirt', 2, 5.00, 10.00, 'tshirt.jpg', 100, 'Cotton T-shirt', 1),
('Novel Book', 3, 2.50, 5.00, 'novel.jpg', 200, 'Bestseller novel', 1),
('Sofa', 4, 150.00, 300.00, 'sofa.jpg', 10, 'Comfortable sofa', 1),
('Football', 5, 8.00, 15.00, 'football.jpg', 40, 'Official size football', 1),
('Toy Car', 6, 3.00, 6.00, 'toycar.jpg', 80, 'Remote control car', 1),
('Running Shoes', 7, 20.00, 40.00, 'shoes.jpg', 60, 'Lightweight running shoes', 1),
('Lipstick', 8, 4.00, 8.00, 'lipstick.jpg', 150, 'Matte finish lipstick', 1),
('Rice Bag', 9, 10.00, 20.00, 'rice.jpg', 30, '5kg rice bag', 1),
('Notebook', 10, 1.00, 2.00, 'notebook.jpg', 300, 'A4 size notebook', 1);

-- Insert sample data into Order
INSERT INTO "sale_order" (order_date_time, total, paid, user_id, remark) VALUES
('2025-08-01 10:00:00', 100.00, 100.00, 1, 'Paid in full'),
('2025-08-02 11:30:00', 50.00, 25.00, 1, 'Partial payment'),
('2025-08-03 09:45:00', 200.00, 200.00, 1, 'Full payment'),
('2025-08-04 15:20:00', 75.00, 0.00, 1, 'Not paid yet'),
('2025-08-05 12:10:00', 300.00, 300.00, 1, 'Paid in cash'),
('2025-08-06 13:55:00', 150.00, 100.00, 1, 'Partial payment'),
('2025-08-07 16:40:00', 60.00, 60.00, 1, 'Paid via card'),
('2025-08-08 08:30:00', 90.00, 0.00, 1, 'Pending'),
('2025-08-09 19:00:00', 110.00, 110.00, 1, 'Paid in full'),
('2025-08-10 17:25:00', 45.00, 45.00, 1, 'Paid in cash');

-- Insert sample data into OrderItem
INSERT INTO sale_order_item (order_id, qty, price) VALUES
(1, 2, 50.00),
(2, 1, 25.00),
(3, 4, 50.00),
(4, 3, 25.00),
(5, 5, 60.00),
(6, 2, 75.00),
(7, 6, 10.00),
(8, 1, 90.00),
(9, 2, 55.00),
(10, 3, 15.00);


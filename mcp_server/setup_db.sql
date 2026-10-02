CREATE DATABASE IF NOT EXISTS quantan_db;
USE quantan_db;

CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS faq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS print_transactions (
    id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100),
    document_name VARCHAR(255),
    pages INTEGER,
    amount DECIMAL(10, 2),
    payment_status VARCHAR(50),
    kiosk_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy data for Categories
INSERT INTO category (name, description) VALUES
('Paper Services', 'Printing and scanning services'),
('Stationery', 'Office supplies and writing materials'),
('Accessories', 'Tech accessories and cables');

-- Insert dummy data for Products
INSERT INTO product (category_id, name, price, description) VALUES
(1, 'A4 Black & White Print', 0.25, 'Standard A4 black and white print per page'),
(1, 'A4 Color Print', 1.00, 'High quality A4 color print per page'),
(2, 'Blue Pen', 2.50, 'Standard ballpoint blue pen'),
(2, 'Notebook', 5.00, 'A5 ruled notebook'),
(3, 'USB-C Cable', 12.00, '1-meter USB-C charging cable');

-- Insert dummy data for FAQs
INSERT INTO faq (question, answer) VALUES
('How do I pay for my prints?', 'You can pay using credit card, debit card, Apple Pay, or Google Pay directly at the kiosk terminal.'),
('What happens if the kiosk is out of paper?', 'Our kiosks are monitored 24/7. If one is out of paper, a technician is automatically dispatched. Please try another nearby kiosk.'),
('Can I print directly from my phone?', 'Yes! You can connect to the kiosk Wi-Fi and print directly, or upload your document to our web portal and scan the generated QR code at the kiosk.');

-- Insert dummy data for Print Transactions
INSERT INTO print_transactions (id, customer_name, document_name, pages, amount, payment_status, kiosk_id) VALUES
('TXN-001', 'Alice Smith', 'Resume.pdf', 2, 0.50, 'Success', 'K-101'),
('TXN-002', 'Bob Jones', 'Board_Presentation.pptx', 15, 3.75, 'Success', 'K-102'),
('TXN-003', 'Charlie Brown', 'Flight_Tickets.pdf', 4, 1.00, 'Pending', 'K-101'),
('TXN-004', 'Diana Prince', 'Tax_Returns_2025.pdf', 30, 7.50, 'Failed', 'K-103'),
('TXN-005', 'Evan Wright', 'Study_Notes.docx', 12, 3.00, 'Success', 'K-101'),
('TXN-006', 'Fiona Gallagher', 'Event_Flyer.pdf', 100, 25.00, 'Success', 'K-102');

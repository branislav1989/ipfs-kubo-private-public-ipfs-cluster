-- Initialize database for IPFS Hosting Platform
CREATE DATABASE ipfs_billing;

-- Connect to the database
\c ipfs_billing;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    balance DECIMAL(20, 8) DEFAULT 0,
    cluster_balance DECIMAL(20, 8) DEFAULT 0,
    total_paid DECIMAL(20, 8) DEFAULT 0,
    email VARCHAR(255),
    api_key VARCHAR(255) UNIQUE
);

-- Create payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    txid VARCHAR(255),
    confirmed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address) REFERENCES customers(address) ON DELETE CASCADE
);

-- Create pins table (public IPFS)
CREATE TABLE IF NOT EXISTS pins (
    id SERIAL PRIMARY KEY,
    cid VARCHAR(255) NOT NULL,
    customer_address VARCHAR(255) NOT NULL,
    size_gb DECIMAL(10, 4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    pin_type VARCHAR(50) DEFAULT 'public',
    FOREIGN KEY (customer_address) REFERENCES customers(address) ON DELETE CASCADE
);

-- Create cluster_pins table (cluster backups with replicas)
CREATE TABLE IF NOT EXISTS cluster_pins (
    id SERIAL PRIMARY KEY,
    cid VARCHAR(255) NOT NULL,
    customer_address VARCHAR(255) NOT NULL,
    size_gb DECIMAL(10, 4) NOT NULL,
    replicas INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    FOREIGN KEY (customer_address) REFERENCES customers(address) ON DELETE CASCADE
);

-- Create bandwidth_usage table
CREATE TABLE IF NOT EXISTS bandwidth_usage (
    id SERIAL PRIMARY KEY,
    customer_address VARCHAR(255) NOT NULL,
    cid VARCHAR(255),
    bytes_transferred BIGINT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_address) REFERENCES customers(address) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_customers_address ON customers(address);
CREATE INDEX IF NOT EXISTS idx_payments_address ON payments(address);
CREATE INDEX IF NOT EXISTS idx_pins_customer ON pins(customer_address);
CREATE INDEX IF NOT EXISTS idx_pins_status ON pins(status);
CREATE INDEX IF NOT EXISTS idx_cluster_pins_customer ON cluster_pins(customer_address);
CREATE INDEX IF NOT EXISTS idx_cluster_pins_status ON cluster_pins(status);
CREATE INDEX IF NOT EXISTS idx_bandwidth_customer ON bandwidth_usage(customer_address);

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE ipfs_billing TO billing_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO billing_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO billing_user;

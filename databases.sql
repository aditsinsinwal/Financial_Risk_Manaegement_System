--Creating Table Assets: Stores information about each asset
CREATE TABLE assets (
  asset_id INT PRIMARY KEY,
  asset_name VARCHAR(255),
  asset_type VARCHAR(50),
  current_value DECIMAL(15, 2)
);
--Creating Table Transactions: Tracks all transactions related to each asset
CREATE TABLE transactions (
  transaction_id INT PRIMARY KEY,
  asset_id INT,
  transaction_date DATE,
  transaction_type VARCHAR(50),
  quantity DECIMAL(10, 2),
  price DECIMAL(15, 2),
  FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);
--Creating Table Portfolios: Defines portfolios that hold various assets
CREATE TABLE portfolios (
  portfolio_id INT PRIMARY KEY,
  portfolio_name VARCHAR(255),
  total_value DECIMAL(15, 2)
);
--Creating Table portfolio_assets: Tracks which assets are in each portfolio and their respective values
CREATE TABLE portfolio_assets (
  portfolio_id INT,
  asset_id INT,
  quantity DECIMAL(10, 2),
  FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id),
  FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

DROP DATABASE IF EXISTS `farmaciapaguepouco`;
CREATE DATABASE `farmaciapaguepouco` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `farmaciapaguepouco`;

CREATE TABLE IF NOT EXISTS `Farmaceutico` (
  `idFarmaceutico` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(100) NOT NULL,
  `CPF` VARCHAR(20) NOT NULL,
  `DataNasc` DATE NOT NULL,
  `Telefone` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`idFarmaceutico`),
  UNIQUE KEY `CPF_UNIQUE` (`CPF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(100) NOT NULL,
  `CPF` VARCHAR(45) NOT NULL,
  `DataNasc` DATE NOT NULL,
  `Telefone` VARCHAR(20) NOT NULL,
  `Endereco` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idCliente`),
  UNIQUE KEY `CPF_UNIQUE` (`CPF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Produtos` (
  `idProdutos` INT NOT NULL AUTO_INCREMENT,
  `Nome` VARCHAR(100) NOT NULL,
  `Composto` VARCHAR(100) NOT NULL,
  `DataValidade` DATE NOT NULL,
  `QuantidadeEstoque` INT NOT NULL,
  `ValorCompra` DECIMAL(10,2) NOT NULL,
  `ValorVenda` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idProdutos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Vendas` (
  `idVendas` INT NOT NULL AUTO_INCREMENT,
  `DataVenda` DATE NOT NULL,
  `Preco` DECIMAL(10,2) NOT NULL,
  `Farmaceutico_idFarmaceutico` INT NOT NULL,
  `Cliente_idCliente` INT NOT NULL,
  PRIMARY KEY (`idVendas`),
  INDEX `idx_vendas_farm` (`Farmaceutico_idFarmaceutico`),
  INDEX `idx_vendas_cli` (`Cliente_idCliente`),
  CONSTRAINT `fk_vendas_farm` FOREIGN KEY (`Farmaceutico_idFarmaceutico`) REFERENCES `Farmaceutico`(`idFarmaceutico`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_vendas_cli`  FOREIGN KEY (`Cliente_idCliente`) REFERENCES `Cliente`(`idCliente`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `Vendas_has_Produtos` (
  `Vendas_idVendas` INT NOT NULL,
  `Vendas_Farmaceutico_idFarmaceutico` INT NOT NULL,
  `Vendas_Cliente_idCliente` INT NOT NULL,
  `Produtos_idProdutos` INT NOT NULL,
  `QuantidadeProduto` INT NOT NULL,
  PRIMARY KEY (`Vendas_idVendas`,`Produtos_idProdutos`),
  INDEX `idx_vhp_prod` (`Produtos_idProdutos`),
  CONSTRAINT `fk_vhp_vendas` FOREIGN KEY (`Vendas_idVendas`) REFERENCES `Vendas`(`idVendas`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_vhp_prod`  FOREIGN KEY (`Produtos_idProdutos`) REFERENCES `Produtos`(`idProdutos`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Produtos` (Nome, Composto, DataValidade, QuantidadeEstoque, ValorCompra, ValorVenda) VALUES
('Aspirina','Ácido Acetilsalicílico','2025-08-10',500,5.00,10.00),
('Paracetamol','Paracetamol','2024-12-15',300,7.50,15.00),
('Ibuprofeno','Ibuprofeno','2023-11-20',200,10.00,20.00),
('Dipirona','Metamizol','2025-05-30',400,6.00,12.00),
('Amoxicilina','Amoxicilina','2024-09-12',150,12.50,25.00);

INSERT INTO `Cliente` (Nome, CPF, DataNasc, Telefone, Endereco) VALUES
('Ana Silva','123.456.789-00','1985-07-12','(11)98765-4321','Rua A, 123'),
('Carlos Oliveira','234.567.890-11','1990-03-23','(21)97654-3210','Rua B, 456');

INSERT INTO `Farmaceutico` (Nome, CPF, DataNasc, Telefone) VALUES
('João da Silva','12345671901','1985-06-15','21987654321'),
('Maria Oliveira','83456789012','1990-07-20','21876543210');

INSERT INTO `Vendas` (DataVenda, Preco, Farmaceutico_idFarmaceutico, Cliente_idCliente) VALUES
('2024-08-01',50.00,1,1),
('2024-08-02',75.00,2,2);

INSERT INTO `Vendas_has_Produtos` (Vendas_idVendas, Vendas_Farmaceutico_idFarmaceutico, Vendas_Cliente_idCliente, Produtos_idProdutos, QuantidadeProduto) VALUES
(1,1,1,1,2),
(2,2,2,2,3);

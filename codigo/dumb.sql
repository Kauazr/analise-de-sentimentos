-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS tb_sentimentos;
USE tb_sentimentos;

-- Tabela: Categorias
DROP TABLE IF EXISTS Categorias;
CREATE TABLE Categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nome_categoria VARCHAR(100) UNIQUE NOT NULL
);

-- Inserção de categorias pré-definidas
INSERT IGNORE INTO Categorias (nome_categoria) VALUES 
    ('Shampoo'),
    ('Condicionador'),
    ('Máscara Capilar'),
    ('Selagem'),
    ('Tintura'),
    ('Botox'),
    ('Progressiva'),
    ('Máscara de Hidratação'),
    ('Óleo'),
    ('Liven'),
    ('Reparador de Ponta'),
    ('Gel Finalizador'),
    ('Spray'),
    ('Pomada Capilar');

-- Tabela: Produtos
DROP TABLE IF EXISTS Produtos;
CREATE TABLE Produtos (
    produto_id INT PRIMARY KEY AUTO_INCREMENT,
    categoria_id INT,
    nome_produto VARCHAR(255) NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id)
);

-- Tabela: AvaliacoesProdutos
DROP TABLE IF EXISTS AvaliacoesProdutos;
CREATE TABLE AvaliacoesProdutos (
    avaliacao_id INT PRIMARY KEY AUTO_INCREMENT,
    produto_id INT,
    texto_avaliacao TEXT NOT NULL,
    sentimento VARCHAR(50) NOT NULL, -- 'positivo', 'neutro', 'negativo'
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES Produtos(produto_id)
);

-- Tabela: FrasesPesquisadas
DROP TABLE IF EXISTS FrasesPesquisadas;
CREATE TABLE FrasesPesquisadas (
    frase_id INT PRIMARY KEY AUTO_INCREMENT,
    texto_frase TEXT NOT NULL,
    sentimento_analisado VARCHAR(50),
    fonte VARCHAR(255) DEFAULT 'Manual',
    data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: Postagens (já existente, será mantida)
DROP TABLE IF EXISTS postagens;
CREATE TABLE postagens (
    id INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(10) NOT NULL,
    texto TEXT NOT NULL,
    sentimento ENUM('positivo', 'neutro', 'negativo') NOT NULL,
    data TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Dados de exemplo para a tabela postagens
INSERT INTO postagens (usuario, texto, sentimento, data) VALUES
('Joao','O produto superou minhas expectativas, estou feliz com a compra.','positivo','2025-04-08 02:10:06'),
('Bia','Adorei o novo recurso, facilitou muito meu trabalho!','positivo','2025-04-08 02:10:06'),
('Thiago','Tudo chegou dentro do prazo e bem embalado, recomendo!','positivo','2025-04-08 02:10:06'),
('Camila','O suporte foi rápido e resolveu meu problema com eficiência.','positivo','2025-04-08 02:10:06'),
('Lucas','Não gostei do serviço, foi uma péssima experiência.','negativo','2025-04-08 02:10:06'),
('Maria','A entrega atrasou e o produto veio danificado.','negativo','2025-04-08 02:10:06'),
('Ricardo','O sistema trava toda hora, estou muito insatisfeito.','negativo','2025-04-08 02:10:06'),
('Paula','Fui mal atendida e não obtive retorno do suporte.','negativo','2025-04-08 02:10:06'),
('Diego','Aplicativo cheio de bugs, impossível de usar.','negativo','2025-04-08 02:10:06'),
('Carlos','Recebi o pedido hoje pela manhã.','neutro','2025-04-08 02:10:06'),
('Lara','O produto chegou conforme descrito no site.','neutro','2025-04-08 02:10:06'),
('Fernanda','Finalizei meu cadastro no sistema.','neutro','2025-04-08 02:10:06'),
('Eduardo','A atualização foi feita ontem à noite.','neutro','2025-04-08 02:10:06'),
('Juliana','Entrei em contato com o suporte para tirar dúvidas.','neutro','2025-04-08 02:10:06'),
('joao','gostei da casa','positivo','2025-05-18 23:39:52');


SELECT * FROM Categorias;

SELECT * FROM postagens;

SELECT * FROM FrasesPesquisadas;

SELECT p.nome_produto, c.nome_categoria 
FROM Produtos p
JOIN Categorias c ON p.categoria_id = c.categoria_id;

SELECT pr.nome_produto, ap.texto_avaliacao, ap.sentimento 
FROM AvaliacoesProdutos ap
JOIN Produtos pr ON ap.produto_id = pr.produto_id;
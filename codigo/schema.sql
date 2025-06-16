-- Estrutura de tabelas para o banco de dados SQLite

-- Tabela: Categorias
DROP TABLE IF EXISTS Categorias;
CREATE TABLE Categorias (
    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT UNIQUE NOT NULL
);

-- Tabela: Produtos
DROP TABLE IF EXISTS Produtos;
CREATE TABLE Produtos (
    produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER,
    nome_produto TEXT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id) ON DELETE CASCADE,
    UNIQUE(categoria_id, nome_produto)
);

-- Tabela: AvaliacoesProdutos
DROP TABLE IF EXISTS AvaliacoesProdutos;
CREATE TABLE AvaliacoesProdutos (
    avaliacao_id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    texto_avaliacao TEXT NOT NULL,
    sentimento TEXT NOT NULL, -- 'positivo', 'neutro', 'negativo'
    data_avaliacao TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES Produtos(produto_id) ON DELETE CASCADE
);

-- Tabela: FrasesPesquisadas
DROP TABLE IF EXISTS FrasesPesquisadas;
CREATE TABLE FrasesPesquisadas (
    frase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    texto_frase TEXT NOT NULL,
    sentimento_analisado TEXT,
    fonte TEXT DEFAULT 'Manual',
    data_adicao TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: Postagens (mantida para compatibilidade, se necessário)
DROP TABLE IF EXISTS postagens;
CREATE TABLE postagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    texto TEXT NOT NULL,
    sentimento TEXT NOT NULL CHECK(sentimento IN ('positivo', 'neutro', 'negativo')),
    data TEXT DEFAULT CURRENT_TIMESTAMP
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
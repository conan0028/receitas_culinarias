-- create database
DROP DATABASE IF EXISTS receitas_culinarias;
CREATE DATABASE receitas_culinarias;

-- 1. Tabelas independentes (sem dependências)
CREATE TABLE cozinheiros (
    cpf_coz VARCHAR(11) PRIMARY KEY,
    nome_coz VARCHAR(80) NOT NULL,
    nome_fantasia VARCHAR(80) NOT NULL,
    dt_contrato_coz DATE NOT NULL,
    salario_coz BIGINT NOT NULL CHECK (salario_coz >= 0)
);

CREATE TABLE degustadores (
    cpf_deg VARCHAR(11) PRIMARY KEY,
    nome_deg VARCHAR(80) NOT NULL,
    dt_contrato_deg DATE NOT NULL,
    salario_deg BIGINT NOT NULL CHECK (salario_deg >= 0)
);

CREATE TABLE editores (
    cpf_edit VARCHAR(11) PRIMARY KEY,
    nome_edit VARCHAR(80) NOT NULL,
    dt_contrato_edit DATE NOT NULL,
    salario_edit BIGINT NOT NULL CHECK (salario_edit >= 0)
);

CREATE TABLE livros (
    titulo_livro VARCHAR(200) PRIMARY KEY,
    isbn INT NOT NULL UNIQUE
);

CREATE TABLE restaurantes (
    nome_rest VARCHAR(80) PRIMARY KEY,
    endereco VARCHAR(200) NOT NULL
);

CREATE TABLE categorias (
    cod_categoria INT PRIMARY KEY,
    desc_categoria VARCHAR(40) NOT NULL
);

CREATE TABLE ingredientes (
    cod_ingred INT PRIMARY KEY,
    nome_ingred VARCHAR(40) NOT NULL
);

CREATE TABLE empregados_rg (
    rg VARCHAR(20) PRIMARY KEY,
    salario BIGINT NOT NULL CHECK (salario >= 0)
);

-- 2. Tabela receitas (depende de várias tabelas)
CREATE TABLE receitas (
    cod_rec INT PRIMARY KEY,
    nome_rec VARCHAR(80) NOT NULL,
    dt_criacao_rec DATE NOT NULL,
    cod_categoria_rec INT NOT NULL,
    cpf_coz VARCHAR(11) NOT NULL,
    isbn_rec INT NOT NULL,
    FOREIGN KEY (cod_categoria_rec) REFERENCES categorias(cod_categoria),
    FOREIGN KEY (cpf_coz) REFERENCES cozinheiros(cpf_coz),
    FOREIGN KEY (isbn_rec) REFERENCES livros(isbn)
);

-- 3. Tabela inclui (deve ser criada imediatamente após receitas)
CREATE TABLE inclui (
    cod_rec_inc INT,
    titulo_liv_inc VARCHAR(200),
    PRIMARY KEY (cod_rec_inc, titulo_liv_inc),
    FOREIGN KEY (cod_rec_inc) REFERENCES receitas(cod_rec),
    FOREIGN KEY (titulo_liv_inc) REFERENCES livros(titulo_livro)
);

-- 4. Demais tabelas dependentes
CREATE TABLE ingredientes_receita (
    cod_rec_ingrec INT,
    cod_ing_ingrec INT,
    quant_ingrec DECIMAL(6, 2) NOT NULL,
    med_ingrec VARCHAR(10) NOT NULL,
    PRIMARY KEY (cod_rec_ingrec, cod_ing_ingrec),
    FOREIGN KEY (cod_rec_ingrec) REFERENCES receitas(cod_rec),
    FOREIGN KEY (cod_ing_ingrec) REFERENCES ingredientes(cod_ingred)
);

CREATE TABLE restaurantes_cozinheiro (
    cod_coz_restcoz VARCHAR(11),
    nome_rest_restcoz VARCHAR(80),
    dt_contratacao DATE NOT NULL,
    PRIMARY KEY (cod_coz_restcoz, nome_rest_restcoz),
    FOREIGN KEY (cod_coz_restcoz) REFERENCES cozinheiros(cpf_coz),
    FOREIGN KEY (nome_rest_restcoz) REFERENCES restaurantes(nome_rest)
);

CREATE TABLE testa (
    cod_rec_test INT,
    cpf_deg_test VARCHAR(11),
    dt_test DATE NOT NULL,
    nota_test BIGINT NOT NULL CHECK (nota_test BETWEEN 0 AND 10),
    PRIMARY KEY (cod_rec_test, cpf_deg_test),
    FOREIGN KEY (cod_rec_test) REFERENCES receitas(cod_rec),
    FOREIGN KEY (cpf_deg_test) REFERENCES degustadores(cpf_deg)
);

CREATE TABLE possui (
    cod_rec_pos INT,
    cpf_edit_pos VARCHAR(11),
    PRIMARY KEY (cod_rec_pos, cpf_edit_pos),
    FOREIGN KEY (cod_rec_pos) REFERENCES receitas(cod_rec),
    FOREIGN KEY (cpf_edit_pos) REFERENCES editores(cpf_edit)
);

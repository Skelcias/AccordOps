CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE document_chunks(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category VARCHAR(150),
    source VARCHAR(255) not null,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL
);


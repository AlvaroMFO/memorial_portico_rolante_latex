# Memorial de Cálculo - Pórtico Rolante

Projeto em LaTeX para documentação completa do dimensionamento de um pórtico rolante (disciplina de Projeto de Máquinas - Engenharia Mecânica).

## Objetivo

Este repositório organiza um memorial de cálculo extenso, com:

- desenvolvimento matemático;
- tabelas e figuras;
- referências normativas e catálogos;
- anexos técnicos.

## Requisitos

### 1) Distribuição LaTeX

- **MiKTeX** (Windows) instalado e atualizado.
- Durante a primeira compilação, o MiKTeX pode solicitar instalação de pacotes ausentes. Recomenda-se habilitar instalação automática de pacotes.

Site oficial:
- [https://miktex.org/download](https://miktex.org/download)

### 2) Ferramenta de build

- `latexmk` (normalmente já disponível no MiKTeX).
- Backend bibliográfico `biber` (também via MiKTeX).

### 3) Editor (opcional, recomendado)

- Cursor/VS Code com extensão **LaTeX Workshop**.
- O projeto já possui configuração em `.vscode/settings.json` para compilar sempre em `output/`.

## Estrutura do projeto

- `main.tex`: arquivo principal do documento.
- `content/sections/`: capítulos e seções do memorial.
- `content/references/`: PDFs de normas/catálogos e `referencias.bib`.
- `assets/images/`: figuras utilizadas no documento.
- `output/`: arquivos gerados na compilação (`.pdf`, `.aux`, `.log`, etc.).

## Como compilar

No terminal, na raiz do projeto:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=output main.tex
```

Saída esperada:

- PDF final em `output/main.pdf`.

## Compilação automática no editor

Este projeto já está configurado para auto build no diretório correto:

- `latex-workshop.latex.outDir = %DIR%/output`
- receita `latexmk` com `-outdir=%DIR%/output`

Arquivo de configuração:

- `.vscode/settings.json`

## Bibliografia

- Arquivo BibTeX/BibLaTeX: `content/references/referencias.bib`.
- As citações no texto usam `\cite{chave}`.
- A lista final é gerada por `\printbibliography` em `main.tex`.

## Fluxo de trabalho recomendado

1. Fazer os cálculos no papel.
2. Transcrever para as seções em `content/sections/`.
3. Adicionar figuras em `assets/images/`.
4. Inserir/atualizar referências em `content/references/referencias.bib`.
5. Compilar e revisar `output/main.pdf`.

## Solução de problemas

- **Pacote LaTeX ausente**: abrir MiKTeX Console, atualizar pacotes e recompilar.
- **Bibliografia não aparece**: verificar se `biber` está instalado e se a chave `\cite{...}` existe no `.bib`.
- **Arquivos aparecendo na raiz**: compilar com `-outdir=output` e manter a receita do LaTeX Workshop ativa.

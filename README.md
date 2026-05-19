# Memorial de Cálculo - Pórtico Rolante

Projeto em LaTeX para documentação completa do dimensionamento de um pórtico rolante (disciplina de Projeto de Máquinas - Engenharia Mecânica).

## Requisitos

### 1) Distribuição LaTeX

- **MiKTeX** (Windows) instalado e atualizado.
- Durante a primeira compilação, o MiKTeX pode solicitar instalação de pacotes ausentes. Recomenda-se habilitar instalação automática de pacotes.

Site oficial:

- [https://miktex.org/download](https://miktex.org/download)

### 2) Formatação automática (obrigatório para formatar no editor)

Para a formatação (`Format Document` / `Format on Save`) funcionar com `latexindent` no Windows, é necessário um Perl completo com módulos extras.

- Instale o **Strawberry Perl**:

```powershell
winget install StrawberryPerl.StrawberryPerl
```

- Instale os módulos Perl exigidos pelo `latexindent`:

```powershell
C:\Strawberry\perl\bin\cpan.bat App::cpanminus
```

```powershell
C:\Strawberry\perl\bin\cpanm.bat YAML::Tiny File::HomeDir Unicode::GCString Log::Log4perl
```

- Feche e abra novamente o Cursor/VS Code após a instalação.

### 3) Editor (opcional, recomendado)

- Cursor/VS Code com extensão **LaTeX Workshop**.
- Cursor/VS Code com extensão **LTeX+** para revisão ortográfica e gramatical em português.
- O projeto já possui configuração em `.vscode/settings.json` para:
  - compilar sempre em `output/`;
  - formatar com `latexindent` usando `perl.exe` + `latexindent.pl` do MiKTeX;
  - habilitar o LTeX em `pt-BR`, com dicionário inicial para termos técnicos do projeto.

## Como compilar

No terminal, na raiz do projeto:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Revisão de texto e gramática (LTeX+)

Necessário instalar a extensão **LTeX+**. [Página de Instalação do LTeX+](https://ltex-plus.github.io/ltex-plus/installation-usage.html#via-editor-extensions)

As marcações aparecem diretamente no editor.
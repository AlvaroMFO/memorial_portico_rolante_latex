"""Corrige camada OCR com caracteres Unicode deslocados em PDFs do Adobe Scan."""

import argparse
import fitz  # PyMuPDF


def fix_char(ch: str) -> str:
    """Corrige um caractere Unicode deslocado."""
    code = ord(ch)

    # Caso observado: 􀁇 = U+100047 -> 'G' = U+0047
    if 0x100000 <= code <= 0x1000FF:
        return chr(code - 0x100000)

    # Outra área privada possível
    if 0xF0000 <= code <= 0xF00FF:
        return chr(code - 0xF0000)

    return ch


def fix_text(text: str) -> str:
    """Corrige caracteres Unicode deslocados em uma string."""
    return "".join(fix_char(ch) for ch in text)


def main():
    """Corrige camada OCR com caracteres Unicode deslocados em PDFs do Adobe Scan."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="PDF de entrada")
    parser.add_argument("-o", "--output", required=True, help="PDF corrigido")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    src = fitz.open(args.input)
    dst = fitz.open()
    total_inserted = 0

    zoom = args.dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page in src:
        rect = page.rect

        # Renderiza a página original como imagem
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        new_page = dst.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, pixmap=pix)

        data = page.get_text("rawdict")
        inserted_count = 0

        for block in data["blocks"]:  # type: ignore
            if block["type"] != 0:  # type: ignore
                continue

            for line in block["lines"]:  # type: ignore
                for span in line["spans"]:  # type: ignore
                    chars = span.get("chars", [])  # type: ignore
                    if not chars:
                        continue

                    text = fix_text("".join(ch["c"] for ch in chars)).strip()
                    if not text:
                        continue

                    x0 = min(ch["bbox"][0] for ch in chars)
                    y0 = min(ch["bbox"][1] for ch in chars)
                    x1 = max(ch["bbox"][2] for ch in chars)
                    y1 = max(ch["bbox"][3] for ch in chars)

                    bbox = fitz.Rect(x0, y0, x1, y1)
                    font_size = max(4, bbox.height * 0.8)
                    baseline = min(bbox.y1, bbox.y0 + font_size)

                    # As caixas do OCR costumam ser apertadas; insert_textbox pode
                    # descartar o texto silenciosamente quando ele nao cabe.
                    new_page.insert_text(
                        fitz.Point(bbox.x0, baseline),
                        text,
                        fontsize=font_size,
                        fontname="helv",
                        render_mode=3,  # invisível, mas pesquisável/copíavel
                    )
                    inserted_count += 1

        if inserted_count == 0:
            raise RuntimeError(
                f"Nenhum texto OCR foi inserido na pagina {page.number + 1}."  # type: ignore
            )
        total_inserted += inserted_count

    dst.save(args.output)
    dst.close()
    src.close()

    print(f"PDF corrigido salvo em: {args.output} ({total_inserted} textos OCR)")


if __name__ == "__main__":
    main()

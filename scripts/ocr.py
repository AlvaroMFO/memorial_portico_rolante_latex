"""Gera PDF pesquisável a partir de uma imagem usando PaddleOCR."""

import os
import argparse

os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
os.environ.setdefault("PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT", "False")

import fitz  # PyMuPDF
from PIL import Image
from paddleocr import PaddleOCR


parser = argparse.ArgumentParser(description="OCR para imagem e geração de PDF pesquisável.")
parser.add_argument("--input", "-i", required=True, help="Imagem de entrada: png, jpg, jpeg etc.")
parser.add_argument("--output", "-o", required=True, help="PDF de saída.")
args = parser.parse_args()


def get_image_size_points(image_path: str, default_dpi: int = 300):
    """Retorna largura e altura da imagem em pontos PDF."""
    with Image.open(image_path) as img:
        width_px, height_px = img.size
        dpi = img.info.get("dpi", (default_dpi, default_dpi))[0] or default_dpi

    width_pt = width_px * 72 / dpi
    height_pt = height_px * 72 / dpi

    return width_px, height_px, width_pt, height_pt


def poly_to_rect(poly, scale_x: float, scale_y: float):
    """Converte polígono do PaddleOCR para retângulo PyMuPDF."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]

    return fitz.Rect(
        min(xs) * scale_x,
        min(ys) * scale_y,
        max(xs) * scale_x,
        max(ys) * scale_y,
    )


def main():
    """Realiza o OCR para a imagem de entrada e salva o resultado no arquivo de saída."""
    input_path = args.input
    output_path = args.output

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_path}")

    if not output_path.lower().endswith(".pdf"):
        raise ValueError("O arquivo de saída deve terminar com .pdf")

    width_px, height_px, width_pt, height_pt = get_image_size_points(input_path)

    scale_x = width_pt / width_px
    scale_y = height_pt / height_px

    ocr = PaddleOCR(
        lang="pt",
        ocr_version="PP-OCRv3",
        device="cpu",
        enable_mkldnn=False,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(input_path)

    doc = fitz.open()
    page = doc.new_page(width=width_pt, height=height_pt)

    page.insert_image(
        fitz.Rect(0, 0, width_pt, height_pt),
        filename=input_path,
    )

    inserted_count = 0

    for ocr_page in result:
        texts = ocr_page["rec_texts"]

        # PaddleOCR v3 costuma retornar rec_polys
        if "rec_polys" in ocr_page:
            boxes = ocr_page["rec_polys"]
        elif "dt_polys" in ocr_page:
            boxes = ocr_page["dt_polys"]
        else:
            raise KeyError("Não encontrei rec_polys nem dt_polys no resultado do OCR.")

        for text, box in zip(texts, boxes):
            if not text.strip():
                continue

            rect = poly_to_rect(box, scale_x, scale_y)

            font_size = max(4, rect.height * 0.75)
            baseline = min(rect.y1, rect.y0 + font_size)

            # OCR boxes can be tight; insert_textbox skips text when it does not fit.
            page.insert_text(
                fitz.Point(rect.x0, baseline),
                text,
                fontsize=font_size,
                fontname="helv",
                render_mode=3,  # texto invisível, mas pesquisável/copíavel
            )
            inserted_count += 1

    if inserted_count == 0:
        raise RuntimeError("OCR nao retornou texto para inserir no PDF.")

    doc.save(output_path)
    doc.close()

    print(f"PDF pesquisável gerado com sucesso: {output_path} ({inserted_count} textos OCR)")


if __name__ == "__main__":
    main()

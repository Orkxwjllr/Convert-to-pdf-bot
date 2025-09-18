import subprocess
import os
import tempfile
import locale

def latex_to_pdf(latex_str: str, output_filename: str = "result.pdf"):
    encoding = locale.getpreferredencoding(False)
    # создаём временную директорию
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, "doc.tex")

        # пишем LaTeX в .tex файл
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(_prepare_latex_to_pdf(latex_str=latex_str))

        # компиляция через pdflatex
        process = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_file],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout_text = process.stdout.decode(encoding, errors="replace")
        stderr_text = process.stderr.decode(encoding, errors="replace")

        # проверка успешности
        if process.returncode != 0:
            print("Ошибка компиляции LaTeX:\n")
            print(stdout_text)
            print(stderr_text)
            raise RuntimeError("Не удалось скомпилировать PDF")

        # копируем PDF в проект
        pdf_file = os.path.join(tmpdir, "doc.pdf")
        os.replace(pdf_file, output_filename)
        print(f"✅ PDF создан: {os.path.abspath(output_filename)}")

def _prepare_latex_to_pdf(latex_str:  str):

    safe_latex_str = latex_str.replace(r"\\", r"\\")

    doc_settings = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage[T2A]{fontenc}
    \usepackage[russian]{babel}
    \usepackage{amsmath}
    """
    begin_doc = r"""\begin{document}"""  
    end_doc = r"""\end{document}"""
    doc = doc_settings+begin_doc+safe_latex_str+end_doc  
    return doc     

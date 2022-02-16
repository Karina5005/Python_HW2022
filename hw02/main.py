import os
import subprocess

from pdflatex import PDFLaTeX


def normalize_input(input_str):
    mlen = max(map(lambda x: len(x), input_str))
    return map(lambda x: x + ['' for _ in range(mlen - len(x))], input_str), mlen


def generate_table(input_str):
    input_str, table_size = normalize_input(input_str)
    return f"\\begin{{center}}\n\\begin{{tabular}}{{{'|' + '|'.join(['c' for _ in range(table_size)]) + '|'}}} \n\\hline\n" \
           + '\n'.join(map(lambda x: ' & '.join(str(field) for field in x) + ' \\\\', input_str)) \
           + "\n\\hline\n\\end{tabular}\n\\end{center}\n"


def generate_picture():
    return "\\begin{center}\n\\includegraphics{universe}\n\\end{center}\n"


def generate_pdf(input_str):
    table = generate_table(input_str)
    picture = generate_picture()
    with open("artifacts\\result.tex", "w") as text_file:
        text_file.write(
            f"\\documentclass{{article}}\n\\usepackage{{graphicx}}\n\\graphicspath{{{{./images/}}}}\n\\begin{{document}}\n"
            + table
            + picture
            + "\\end{document}")
    os.system("pdflatex result.tex")

if __name__ == '__main__':
    generate_pdf([["cell1", "cell2", "cell3"], ["cell1", "cell2"], ["cell1", "cell2", "cell3"]])

import sys
import os
import difflib
from PyPDF2 import PdfFileReader, PdfFileWriter


def handle_ppt_in_pdf(file_path: str):
    if not os.path.isfile(file_path):
        print("请给定有效路径")
        exit(1)
    arr = os.path.splitext(file_path)
    file_out_path = arr[0] + ".去重复" + arr[1]
    with open(file_path, 'rb') as pdf, open(file_out_path, "wb") as pdfOut:
        pdfReader = PdfFileReader(pdf)
        writer = PdfFileWriter()
        pagesCount = pdfReader.getNumPages()
        prePage = None
        for pageId in range(pagesCount):
            page = pdfReader.getPage(pageId)
            print("%3d/%3d ... %d %%" % (pageId, pagesCount,
                                         ((pageId) / float(pagesCount)) * 100))
            if prePage is not None:
                if difflib.SequenceMatcher(None, prePage.extractText().strip(), page.extractText().strip()).quick_ratio() <= 0.95:
                    writer.addPage(prePage)
            prePage = page
        writer.addPage(prePage)
        print('正在写入...请勿退出...')
        writer.write(pdfOut)
        print('写入文件完成.')
        print('已保存到: ' + file_out_path)


def main():
    if len(sys.argv) == 1:
        print("请给定一个PDF文件.")
        exit(1)
    handle_ppt_in_pdf(sys.argv[1])


if __name__ == '__main__':
    main()

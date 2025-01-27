import logging
import os
import subprocess

from bs4 import BeautifulSoup
from ebooklib import epub
from ebooklib.epub import EpubHtml

from pathlib import Path

from feed_utils.anything_llm_feed import do_feed_books


def convert_azw3_to_epub(azw3_f, epub_f):
    """使用 Calibre 将 .azw3 文件转换为 .epub 文件。"""
    try:
        subprocess.run(["C:\Program Files\Calibre2\ebook-convert.exe", azw3_f, epub_f], check=True, capture_output=True, text=True)
        # 添加 capture_output 和 text
        logging.info(f"成功将 {azw3_f} 转换为 {epub_f}")
    except subprocess.CalledProcessError as e:
        # 打印错误信息
        logging.error(f"转换 {azw3_f} 到 {epub_f} 时出错: {e.stderr}")
        return None

    return epub_f


def read_epub_content(epub_f):
    try:
        book = epub.read_epub(epub_f)

        # 获取元数据
        epub_title = book.get_metadata('DC', 'title')[0][0]
        epub_author = book.get_metadata('DC', 'creator')[0][0]

        logging.debug(f"书名: {epub_title}, 作者: {epub_author}")

        text_content = []
        for item in book.get_items():
            if isinstance(item, EpubHtml):  # 检查是否为HTML文档
                epub_content = item.get_content().decode('utf-8')
                soup = BeautifulSoup(epub_content, 'html.parser')
                text_content.append(soup.get_text())

        return epub_title, epub_author, "\n".join(text_content)

    except Exception as e:
        logging.error(f"读取 EPUB 文件出错: {e}")
        return None, None, None


def feed_all_books(settings):
    # 使用 Path 对象
    path = Path(settings['book_path'])
    # 使用 glob 匹配所有 .azw3 文件
    azw3_files = list(path.rglob('*.azw3'))
    total_count = len(azw3_files)
    logging.info(f"文件总数：{total_count}")
    idx = 1
    batch_files = []
    for file in azw3_files:
        if file.name.endswith(".azw3"):
            logging.info(f"Processing {idx}/{total_count}, {file}")
            idx += 1

            azw3_f = os.path.join(path, file.name)
            epub_f = os.path.join(path, file.name.replace(".azw3", ".epub"))
            txt_f = os.path.join(path, file.name.replace(".azw3", ".txt"))
            f = convert_azw3_to_epub(azw3_f, epub_f)
            if f is None:
                logging.error(f"转换 {azw3_f} 到 {epub_f} 时出错")
                continue

            title, author, content = read_epub_content(epub_f)
            if title is None or author is None or content is None:
                logging.error(f"读取 {epub_f} 时出错")
                continue

            os.remove(epub_f)

            with open(txt_f, 'w', encoding='utf-8') as txt_file:
                txt_file.write(f"title: {title}\n")
                txt_file.write(f"author: {author}\n")
                txt_file.write(content)

            logging.debug(f"book: {epub_f}, 书名: {title}, 作者: {author}")

            batch_files.append(txt_f)
            if batch_files.__len__() >= settings['batch_size']:
                do_feed_books(batch_files)

            for f in batch_files:
                os.remove(f)

            batch_files.clear()

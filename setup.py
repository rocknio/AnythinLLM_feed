import os
import subprocess
from pathlib import Path

from setuptools import setup
from Cython.Build import cythonize
from setuptools import find_packages

exclude = [
    "__init__.py",
    "setup.py"
]


def compile_all_py(path):
    # 使用 Path 对象
    path = Path(path)
    # 使用 glob 匹配所有 .azw3 文件
    py_files = list(path.rglob('*.py'))
    for py_file in py_files:
        if os.path.basename(py_file) in exclude:
            continue

        # 编译 .py 文件
        # cythonize(str(py_file), language_level=3)
        subprocess.run(["C:\\Python312\\Scripts\\cythonize.exe", "-3", "-b", "-i", py_file], check=True, capture_output=True, text=True)
        print(f"Compiled {py_file}")

    delete_c_files(py_files)


# 自动删除生成的 .c 文件
def delete_c_files(py_files):
    for py_file in py_files:
        c_file = os.path.splitext(py_file)[0] + '.c'
        if os.path.exists(c_file):
            os.remove(c_file)
            print(f"Deleted {c_file}")


if __name__ == '__main__':
    compile_all_py(os.path.dirname(os.path.abspath(__file__)))

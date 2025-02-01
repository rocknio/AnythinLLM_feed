from setuptools import setup, Extension
from Cython.Build import cythonize
import os


# 获取所有需要编译的 .py 文件
def get_py_files(path):
    all_py_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and file not in exclude:
                all_py_files.append(os.path.join(root, file))
    return all_py_files


exclude = [
    "__init__.py",
    "setup.py",
    "run.py"
]

# 获取所有 .py 文件
py_files = get_py_files(os.path.dirname(os.path.abspath(__file__)))

# 创建扩展模块
extensions = [
    Extension(
        name=os.path.splitext(os.path.relpath(py_file, start=os.path.dirname(os.path.abspath(__file__))))[0].replace(os.sep, '.'),
        sources=[py_file]
    ) for py_file in py_files
]

setup(
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
)

for py_file in py_files:
    c_file = os.path.splitext(py_file)[0] + '.c'
    if os.path.exists(c_file):
        os.remove(c_file)
        print(f"Deleted {c_file}")

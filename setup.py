import setuptools
import clarisse

with open("README.md","r",encoding="utf-8") as fh:
    long_description=fh.read()

print("version={0}".format(clarisse.version))

setuptools.setup(
        name="clarisse",
        license="Apache 2.0",
        version=clarisse.version[1:],
        author="Lightyears",
        author_email="1MLightyears@gmail.com",
        description="A light-weighted GUI framework for Python programs.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/1MLightyears/clarisse',
        classifiers=[
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
            "Development Status :: 2 - Pre-Alpha",
            "License :: OSI Approved :: Apache Software License",
            "Natural Language :: English"
        ],
        install_requires=[
            "PySide2"
        ],
        python_requires='>=3.6',
        packages=setuptools.find_packages(),
)


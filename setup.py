import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="staticPageServer-hydrogen602",
    version="0.0.1",
    author="hydrogen602",
    author_email="hydrogen31415@gmail.com",
    description="A package to quickly host a folder as a local server for developing webpages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hydrogen602/simpleServer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

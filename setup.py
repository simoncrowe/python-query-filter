import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="query-filter",
    version="1.0.0",
    author="Simon Crowe",
    author_email="simon.r.crowe@pm.me",
    description="Python's filter function with composable queries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simoncrowe/python-query-filter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

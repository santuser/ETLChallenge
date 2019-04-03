import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="challenge_etl_module",
    version="0.0.1",
    author="Santiago Nahuel Peron",
    author_email="santiago.peron.acc@gmail.com",
    description="ETL package created to process text files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
)

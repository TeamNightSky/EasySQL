import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easysql",
    version="1.0.1",
    author="TeamNightSky",
    description="Python SQL query generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeamNightSky/EasySQL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: SQL",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Database",
    ],
    python_requires=">=3.6",
)

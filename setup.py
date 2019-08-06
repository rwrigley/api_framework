import setuptools

setuptools.setup(
    name="api_framework",
    version="0.0.4",
    author="Ryan Wrigley",
    author_email="ryan@servicefusion.com    ",
    description="REST API framework based on peewee, marshmallow, falcon",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/rwrigley/api_framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
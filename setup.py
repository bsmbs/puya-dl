import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="puya-dl", # Replace with your own username
    version="1.1.1",
    author="pizza61",
    author_email="2006mappa@protonmail.com",
    description="Short Python script and GUI for batch downloading PuyaSubs releases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pizza61/puya-dl",
    project_urls={
        "Bug Tracker": "https://github.com/pizza61/puya-dl/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: Qt"
    ],
    packages=['puyadl'],
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
        'PySide6>=6.0.2'
    ],
    python_requires=">=3.6"
)
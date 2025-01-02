"""Setup configuration for the java-dependency-viewer package."""

from setuptools import setup, find_packages

setup(
    name="java-dependency-viewer",
    version="0.1.0",
    description="A CLI tool for analyzing Java class dependencies using javap.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Hiromichi Hayashi",
    author_email="6phyphy6@gmail.com",
    url="https://github.com/payashi/java-dependency-viewer",
    license="MIT",
    packages=find_packages(),
    package_data={
        "java_dependency_viewer": ["templates/*.html"],
    },
    install_requires=[
        "networkx>=2.5",
    ],
    entry_points={
        "console_scripts": [
            "jdv=java_dependency_viewer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

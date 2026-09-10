"""
UCPF — Universal Consciousness and Physics Framework
Setup script for pip installation.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ucpf",
    version="10.1.0",
    author="UPE-78 Research Collective",
    author_email="research@upe78.system",
    description="A rigorous, falsifiable framework for anomalous propulsion and vacuum-coupled phenomena",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joshoshfield-a11y/upe78-knowledge-base",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black>=22.0", "flake8>=4.0"],
        "viz": ["matplotlib>=3.4.0"],
    },
    keywords="physics uap propulsion plasma vacuum casimir alfven falsification",
    project_urls={
        "Bug Reports": "https://github.com/joshoshfield-a11y/upe78-knowledge-base/issues",
        "Source": "https://github.com/joshoshfield-a11y/upe78-knowledge-base",
        "Documentation": "https://github.com/joshoshfield-a11y/upe78-knowledge-base/wiki",
    },
)

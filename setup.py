from setuptools import setup, find_packages

setup(
    name="edu_pad",
    version="0.0.1",
    author="Simon Lara",
    author_email="simon.lara@est.iudigital.edu.co",
    description="Este proyecto es para hacer scrapeo a la pagina web de panamericana",
    install_requires=[
        "pandas",
        "requests",
        "streamlit",
        "beautifulsoup4",
        "openpyxl",
        "lxml"
    ]
)
import setuptools

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mri2fem", # Replace with your own username
    version="0.1",
    author="KA Mardal, ME Rognes, TB Thompson, LM Valnes",
    author_email="meg@simula.no",
    description="Mathematical Modeling of the Human Brain Software",
    long_description=long_description,
    long_description_content_type="text",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.1',
)

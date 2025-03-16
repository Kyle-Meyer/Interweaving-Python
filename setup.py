from setuptools import setup, find_packages

setup(
    name="signal-untangler",
    version="0.1.0",
    packages=find_packages(),
    description="A module for untangling interleaved signal patterns",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/signal-untangler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

from setuptools import setup, find_packages
setup(
    name="datahosting-ipfs",
    version="1.0.0",
    author="Branislav Usjak",
    author_email="branislavusjak1989@gmail.com",
    description="Python SDK for DataHosting IPFS hosting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/branislav1989/ipfs-kubo-private-public-ipfs-cluster",
    packages=find_packages(),
    install_requires=["requests>=2.28.0"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

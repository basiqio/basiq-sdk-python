from setuptools import setup
setup(
    name="basiq",
    packages=["basiq/services", "basiq/utils", "basiq"],
    version="1.0.1",
    description="SDK Package for Basiq's HTTP API",
    author="Nenad Lukic",
    python_requires=">=3",
    install_requires=["requests"],
    author_email="nenad@basiq.io",
    url="https://github.com/basiqio/basiq-sdk-python",
    download_url="https://github.com/basiqio/basiq-sdk-python/archive/1.0.1.tar.gz",
    keywords=["basiq", "finance", "sdk", "api"],
    classifiers=[]
)

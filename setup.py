from setuptools import find_packages, setup

from jffe import get_version

setup(
    name="jffe",
    version=get_version() or "0.0.1",
    description="Just For Fun Examples",
    author="Toxa Yantsen",
    license="MIT License",
    packages=find_packages(
        exclude=(
            "tests",
            "tests.*",
        )
    ),
    install_requires=[
        "pydantic~=2.10.6",
        "aiohttp~=3.13.2",
        "PyYAML~=6.0.2",
    ],
    zip_safe=False,
)

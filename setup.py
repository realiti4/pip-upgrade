import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pip-upgrade-tool",
    version="0.6.4",
    author="Onur Cetinkol",
    author_email="realiti44@gmail.com",
    description="An easy tool for upgrading all of your packages while not breaking dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/realiti4/pip-upgrade",
    entry_points = {
        'console_scripts': ['pip-upgrade = pip_upgrade:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=["pip_upgrade", "pip_upgrade.tools"],
    install_requires=["packaging"],
)

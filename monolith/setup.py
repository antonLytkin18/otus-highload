from setuptools import setup, find_packages

setup(
    name='app',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)

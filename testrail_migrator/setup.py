from setuptools import find_packages, setup

setup(
    name='testrail-migrator',
    version='0.1',
    description='Plugin to migrate your data from testrail',
    install_requires=['PyYAML', 'tqdm'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

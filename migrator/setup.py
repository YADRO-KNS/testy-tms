from setuptools import find_packages, setup

# TODO: remake requirements so testy is needed
setup(
    name='testrail-migrator',
    version='0.1',
    description='Plugin to migrate your data from testrail',
    install_requires=['PyYAML', 'tqdm', 'requests', 'celery', 'aiohttp'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

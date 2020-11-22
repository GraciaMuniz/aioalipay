from setuptools import setup, find_packages


setup(
    name='aioalipay',
    version='0.1',
    description='Asyncio-based client for Alipay Platform',
    author='Rocky Feng',
    author_email='folowing@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['aiohttp>=3.6.2'],
    zip_safe=False,
)

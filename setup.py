try:
    from setuptools import setup
except  ImportError:
    from distutils.core import setup


config = {
    'description': 'MDD_To_XML_Tables',
    'author': 'Daniel Mladenov',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'DanielPlamenovMldenov@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': ['bin/exm11.py'],
    'name': 'MDD_To_XML_Tables'
}

setup(**config)

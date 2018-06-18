import re
import setuptools

try:
    with open('./django_urr/__init__.py', 'r') as infp:
        version = re.search("__version__ = ['\"]([^'\"]+)['\"]", infp.read()).group(1)
except IOError:
    version = 'unknown'


dev_dependencies = [
    'flake8',
    'isort',
    'pydocstyle',
    'pytest-cov',
    'pytest-django>=3.0.0',
]

if __name__ == '__main__':
    setuptools.setup(
        name='django-urr',
        description='URL resolver utilities for Django',
        version=version,
        url='https://github.com/valohai/django-urr',
        author='Valohai',
        author_email='info@valohai.com',
        maintainer='Aarni Koskela',
        maintainer_email='akx@iki.fi',
        license='MIT',
        install_requires=['Django'],
        tests_require=dev_dependencies,
        extras_require={'dev': dev_dependencies},
        packages=setuptools.find_packages('.', exclude=('urrtests',)),
    )

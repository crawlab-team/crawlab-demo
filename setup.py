from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    install_requires = f.read().split('\n')

setup(
    name='crawlab-demo',
    version='0.0.6-9',
    packages=find_packages(),
    url='https://github.com/crawlab-team/crawlab-demo',
    license='BSD-3-Clause',
    author='tikazyq',
    author_email='tikazyq@163.com',
    description='Demo for Crawlab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'crawlab-demo=crawlab_demo.cli.main:main'
        ]
    }
)

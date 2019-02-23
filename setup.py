from setuptools import setup, find_packages


def main():
    setup(
        name='asynconsumer',
        version='1.0.5',
        url='https://github.com/rhoboro/asynconsumer',
        license='Apache License 2.0',
        author='rhoboro',
        author_email='rhoboro@gmail.com',
        maintainer='rhoboro',
        maintainer_email='rhoboro@gmail.com',
        description='asynconsumer is a simple library for processing each items within iterable using asyncio.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[],
        extras_require={
        },
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
    )


if __name__ == '__main__':
    main()

from setuptools import setup, find_packages


def main():
    setup(
        name='asynconsumer',
        version='1.0.1',
        url='https://github.com/rhoboro/asynconsumer',
        license='Apache License 2.0',
        author='rhoboro',
        author_email='rhoboro@gmail.com',
        maintainer='rhoboro',
        maintainer_email='rhoboro@gmail.com',
        packages=find_packages(),
        install_requires=[],
        extras_require={
        },
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )


if __name__ == '__main__':
    main()

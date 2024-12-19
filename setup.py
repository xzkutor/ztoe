from setuptools import setup, find_packages

setup(
    name='ztoe',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'beautifulsoup4',
        'pytest',
        'pytest-asyncio',
        'pytest-aiohttp',
    ],
    entry_points={
        'console_scripts': [
            'ztoe-client=ztoe.client:main',
        ],
    },
    author='Andrii Mozharovsky',
    author_email='am@swordfish.name',
    description='A package for handling ZTOE schedules',
    url='https://github.com/xzkutor/ztoe',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
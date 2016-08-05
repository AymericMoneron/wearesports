from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='wearesports',
    version='0.1',
    description='WeAreSports Command-line interface',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='wearesports sports booking command-line cli',
    url='http://github.com/AymericMoneron/wearesports',
    author='Aymeric MONERON',
    author_email='aymeric.moneron@gmail.com',
    license='MIT',
    packages=['wearesports'],
    entry_points={
        'console_scripts': ['wearesports=wearesports.shell:main']
    },
    install_requires=[
        'beautifulsoup4',
        'PTable',
        'requests'
    ],
    zip_safe=False)

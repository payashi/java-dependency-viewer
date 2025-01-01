from setuptools import setup, find_packages

setup(
    name='java-dependency-viewer',
    version='0.1.0',
    description='A CLI tool for analyzing Java class dependencies using javap.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='6phyphy6@gmail.com',
    url='https://github.com/payashi/java-dependency-viewer',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'java-dependency-viewer = java_dependency_viewer.viewer:analyze_class_file',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

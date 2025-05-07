from setuptools import setup, find_packages

setup(
    name="betelgeuse-simulator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pygame>=2.5.2',
        'numpy>=1.24.3',
        'tensorflow>=2.14.0',
        'imageio>=2.31.5',
        'scikit-learn>=1.3.2',
        'matplotlib>=3.8.1',
        'scipy>=1.11.3',
        'pandas>=2.1.2',
        'torch>=2.1.0',
        'transformers>=4.34.1',
    ],
    author="Your Name",
    description="Betelgeuse Evolution AI Simulator",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
)
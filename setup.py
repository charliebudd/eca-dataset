from setuptools import setup, find_packages

setup(
    name='ecadataset',
    version='0.1.0',
    description='Python loader for the Endoscopic Content Area (ECA) dataset.',
    author='Charlie Budd',
    author_email='charles.budd@kcl.ac.uk',
    url='https://github.com/charliebudd/torch-content-area',
    license='MIT',
    package_dir={'':'src'},
    packages=['eca'],
    install_requires=['synapseclient', 'pillow']
)

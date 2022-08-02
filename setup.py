from setuptools import setup
import versioneer

with open("README.md") as file:
    long_description = file.read()

setup(
    name='ecadataset',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Python loader for the Endoscopic Content Area (ECA) dataset.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Charlie Budd',
    author_email='charles.budd@kcl.ac.uk',
    url='https://github.com/charliebudd/eca-dataset',
    license='MIT',
    package_dir={'':'src'},
    packages=['eca'],
    scripts=['bin/download-eca'],
    install_requires=['synapseclient', 'pillow', 'numpy']
)

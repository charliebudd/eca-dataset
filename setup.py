from setuptools import setup

setup(
    name='ecadataset',
    version='0.1.0',
    description='Python loader for the Endoscopic Content Area (ECA) dataset.',
    author='Charlie Budd',
    author_email='charles.budd@kcl.ac.uk',
    url='https://github.com/charliebudd/eca-dataset',
    license='MIT',
    package_dir={'':'src'},
    packages=['eca'],
    scripts=['bin/download-eca'],
    install_requires=['synapseclient', 'pillow', 'numpy'],
    test_suite='tests',
    tests_require=['parameterized', 'Surface-Distance-Based-Measures@git+https://github.com/deepmind/surface-distance.git']
)

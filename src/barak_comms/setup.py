from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'barak_comms'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='MERL',
    maintainer_email='info@merl.lab',
    description='Secure telemetry node.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'secure_telemetry = barak_comms.secure_telemetry:main',
        ],
    },
)

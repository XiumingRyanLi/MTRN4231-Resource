import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'tf2_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'rviz'),
            glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ryan',
    maintainer_email='ryan.li20180211@gmail.com',
    description='MTRN4231 Lab 2 demo: TF2 tree for a camera-to-base_link target lookup',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_broadcaster = tf2_demo.camera_broadcaster:main',
            'target_publisher = tf2_demo.target_publisher:main',
            'target_locator = tf2_demo.target_locator:main',
        ],
    },
)

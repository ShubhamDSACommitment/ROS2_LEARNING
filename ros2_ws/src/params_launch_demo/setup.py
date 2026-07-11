import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'params_launch_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # install the launch/ folder so `ros2 launch` can find the .launch.py files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shubham',
    maintainer_email='shubhamyadav.cdac11@gmail.com',
    description='Lesson 05+06: parameters and launch files.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'robot = params_launch_demo.configurable_robot:main',
        ],
    },
)

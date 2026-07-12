from setuptools import find_packages, setup

package_name = 'tf2_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shubham',
    maintainer_email='shubhamyadav.cdac11@gmail.com',
    description='Lesson 08: TF2 broadcaster + listener.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'broadcaster = tf2_demo.frame_broadcaster:main',
            'listener = tf2_demo.frame_listener:main',
        ],
    },
)

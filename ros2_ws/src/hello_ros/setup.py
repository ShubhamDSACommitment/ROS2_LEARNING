from setuptools import find_packages, setup

package_name = 'hello_ros'

# setup.py = the Python build script for an ament_python package.
setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # 1) register this package in the ROS 2 package index (so `ros2` can find it)
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        # 2) install the manifest
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shubham',
    maintainer_email='shubhamyadav.cdac11@gmail.com',
    description='Lesson 02: my first ROS 2 package + node.',
    license='MIT',
    entry_points={
        # THIS creates the "executable" you launch with `ros2 run`.
        #   '<exe-name> = <python.module.path>:<function>'
        # so:  ros2 run hello_ros hello   ->   runs hello_ros/hello_node.py :: main()
        'console_scripts': [
            'hello = hello_ros.hello_node:main',
        ],
    },
)

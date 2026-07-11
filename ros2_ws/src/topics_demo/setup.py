from setuptools import find_packages, setup

package_name = 'topics_demo'

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
    description='Lesson 03: publisher + subscriber over a topic.',
    license='MIT',
    entry_points={
        'console_scripts': [
            # producer: publishes robot status heartbeats
            'status_pub = topics_demo.robot_status_publisher:main',
            # consumer: subscribes and logs them (like the fleet manager)
            'status_monitor = topics_demo.status_monitor:main',
        ],
    },
)

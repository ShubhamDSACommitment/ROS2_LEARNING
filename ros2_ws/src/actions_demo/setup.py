from setuptools import find_packages, setup

package_name = 'actions_demo'

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
    description='Lesson 07: action server + client.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'fib_server = actions_demo.fib_server:main',
            'fib_client = actions_demo.fib_client:main',
        ],
    },
)

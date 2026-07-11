from setuptools import find_packages, setup

package_name = 'services_demo'

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
    description='Lesson 04: service server + client (request/response).',
    license='MIT',
    entry_points={
        'console_scripts': [
            'power_server = services_demo.robot_power_server:main',  # the server (endpoint)
            'power_client = services_demo.power_client:main',        # the client (caller)
        ],
    },
)

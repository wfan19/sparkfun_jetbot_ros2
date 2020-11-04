from setuptools import setup

package_name = 'sparkfun_jetbot_ros2'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Bill Fan',
    maintainer_email='billfan.2001@gmail.com',
    description='ROS2 package for controlling a Sparkfun Jetbot\'s motors',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'jetbot_drive = sparkfun_jetbot_ros2.jetbot_drive:main',
        ],
    },
)

from setuptools import find_packages, setup

package_name = 'robot_actions'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ilyas',
    maintainer_email='ilyassilyass@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'battery_charger = robot_actions.battery_charger:main',
            'battery_client = robot_actions.battery_client:main',
            'battery_charger_queue = robot_actions.battery_charger_queue:main',
            'battery_charger_preempt = robot_actions.battery_charger_preempt:main',
            'battery_charger_reject = robot_actions.battery_charger_reject:main',
        ],
    },
)

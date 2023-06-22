from setuptools import setup

package_name = 'robot_manipulator'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yesopi',
    maintainer_email='y.pineros@uniandes.edu.co',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'interfaz_brazo=robot_manipulator.robot_manipulator_interface_node:main',
        'pub=robot_manipulator.test_position_publisher_node:main',
        'teclado_brazo =robot_manipulator.manipulator:main',
        'serial_brazo =robot_manipulator.serial_manipulator_node:main',
        'inversa=robot_manipulator.cinematica_inversa:main',
        'player=robot_manipulator.player:main',
        'player_viejo=robot_manipulator.player_viejo:main',
        'perception=robot_manipulator.master_percepcion:main'
        ],
    },
)

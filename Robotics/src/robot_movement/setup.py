from setuptools import setup

package_name = 'robot_movement'

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
        'console_scripts': ['teclado=robot_movement.robot_teleop:main',
        'esp32=robot_movement.esp32:main',
        'interfaz=robot_movement.robot_interface:main',
        'player=robot_movement.robot_player:main',
        'serial=robot_movement.serialtest:main',
        
        ],
    },
)

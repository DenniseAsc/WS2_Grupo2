from setuptools import setup
from glob import glob
import os
package_name = 'ws2_g2'
setup(name=package_name, version='0.1.0', packages=[package_name],
    data_files=[('share/ament_index/resource_index/packages', ['resource/' + package_name]),
                ('share/' + package_name, ['package.xml']),
                (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
                (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
                (os.path.join('share', package_name, 'config'), glob('config/*'))],
    install_requires=['setuptools'], zip_safe=True,
    maintainer='grupo2', maintainer_email='grupo2@example.com',
    description='Workshop 2: robot diferencial y trayectoria del numero 2',
    license='Apache-2.0', entry_points={'console_scripts': ['trayectoria_2 = ws2_g2.trayectoria_2:main']})

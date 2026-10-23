import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory('ws2_g2')
    gz_pkg = get_package_share_directory('ros_gz_sim')
    urdf = os.path.join(pkg, 'urdf', 'robot.urdf')
    with open(urdf, encoding='utf-8') as file:
        description = file.read()
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(gz_pkg, 'launch', 'gz_sim.launch.py')),
            launch_arguments={'gz_args': '-r empty.sdf'}.items()),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': description, 'use_sim_time': True}], output='screen'),
        TimerAction(period=5.0, actions=[Node(package='ros_gz_sim', executable='create',
            arguments=['-topic', '/robot_description', '-name', 'WS2_G2', '-z', '0.04'], output='screen')]),
        Node(package='ros_gz_bridge', executable='parameter_bridge',
             parameters=[{'config_file': os.path.join(pkg, 'config', 'bridge.yaml')}], output='screen'),
    ])

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('four_wheel_robot')
    xacro_file = os.path.join(pkg, 'urdf', 'four_wheel_robot.urdf.xacro')
    world_file = os.path.join(pkg, 'worlds', 'room.world')
    robot_description = xacro.process_file(xacro_file).toxml()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')),
        launch_arguments={'world': world_file}.items())

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
        output='screen')

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'four_wheel_robot', '-z', '0.1'],
        output='screen')

    jsb = Node(package='controller_manager', executable='spawner',
               arguments=['joint_state_broadcaster'])
    ddc = Node(package='controller_manager', executable='spawner',
               arguments=['diff_drive_controller'])

    return LaunchDescription([
        gazebo,
        rsp,
        spawn,
        RegisterEventHandler(OnProcessExit(target_action=spawn, on_exit=[jsb])),
        RegisterEventHandler(OnProcessExit(target_action=jsb, on_exit=[ddc])),
    ])

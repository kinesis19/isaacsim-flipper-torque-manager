import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # 파일들이 있는 패키지 이름
    pkg_name = 'orion_moveit_config'

    # 컨트롤러 설정 파일 경로
    controllers_yaml_path = os.path.join(get_package_share_directory(pkg_name), 'config', 'orion_controllers.yaml')
    
    # URDF 파일 로드 (XACRO 처리 포함)
    urdf_xacro_path = os.path.join(get_package_share_directory(pkg_name), 'config', 'orion.urdf.xacro')
    robot_description_config = xacro.process_file(urdf_xacro_path)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # Robot State Publisher 노드
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )
    
    # ros2_control을 위한 컨트롤러들을 실행(spawn)하는 노드들
    # joint_state_broadcaster 스포너
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "-c", "/controller_manager"],
    )
    
    # 플리퍼 컨트롤러 스포너 (YAML과 이름 일치)
    flipper_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["flipper_controller", "-c", "/controller_manager"],
    )

    # 바퀴 컨트롤러 스포너
    track_velocity_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["track_velocity_controller", "-c", "/controller_manager"],
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_broadcaster_spawner,
        flipper_controller_spawner,
        track_velocity_controller_spawner,
    ])
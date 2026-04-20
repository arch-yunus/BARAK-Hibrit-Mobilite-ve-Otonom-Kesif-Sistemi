from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # 1. Perception Node (Mergen-Vision)
        Node(
            package='barak_perception',
            executable='vision_processor',
            name='vision_processor_node',
            output='screen',
            parameters=[{'use_sim_time': True}]
        ),
        
        # 2. Navigation Node (Umay-Core)
        Node(
            package='barak_navigation',
            executable='path_planner',
            name='path_planner_node',
            output='screen'
        ),
        
        # 3. Locomotion Node (Toghrul-Drive)
        Node(
            package='barak_locomotion',
            executable='drive_controller',
            name='drive_controller_node',
            output='screen'
        ),
        
        # 4. Communication Node (Secure Comms)
        Node(
            package='barak_comms',
            executable='secure_telemetry',
            name='secure_telemetry_node',
            output='screen'
        ),
        
        # 5. Robot State Publisher (Description)
        # Note: This usually requires a xacro processing step
        # Placeholder for brevity, but logically part of bringup
    ])

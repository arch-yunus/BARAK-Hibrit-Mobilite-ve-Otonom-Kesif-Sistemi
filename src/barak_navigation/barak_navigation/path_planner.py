import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Path
from barak_common.msg import HybridState

class PathPlanner(Node):
    def __init__(self):
        super().__init__('path_planner')
        self.get_logger().info('Umay-Core Path Planner Initialized')
        
        # Subscriptions
        self.state_sub = self.create_subscription(
            HybridState,
            'barak/terrain_info',
            self.terrain_callback,
            10
        )
        
        self.goal_sub = self.create_subscription(
            PoseStamped,
            'goal_pose',
            self.goal_callback,
            10
        )
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )
        
        self.path_pub = self.create_publisher(
            Path,
            'barak/global_path',
            10
        )
        
        self.current_state = HybridState()

    def terrain_callback(self, msg):
        self.current_state = msg
        self.get_logger().debug(f'Terrain updated: Mode {msg.current_mode}')

    def goal_callback(self, msg):
        self.get_logger().info(f'New goal received: {msg.pose.position.x}, {msg.pose.position.y}')
        
        # Simple straight-line path generation (Placeholder for Umay-Core logic)
        path = Path()
        path.header.stamp = self.get_clock().now().to_msg()
        path.header.frame_id = 'map'
        
        # Logic would go here to account for Air/Land/Water modes
        if self.current_state.current_mode == HybridState.MODE_AIR:
            self.get_logger().info('Planning aerial route...')
        elif self.current_state.current_mode == HybridState.MODE_WATER:
            self.get_logger().info('Planning maritime route...')
        else:
            self.get_logger().info('Planning terrestrial route...')

        self.path_pub.publish(path)

def main(args=None):
    rclpy.init(args=args)
    node = PathPlanner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

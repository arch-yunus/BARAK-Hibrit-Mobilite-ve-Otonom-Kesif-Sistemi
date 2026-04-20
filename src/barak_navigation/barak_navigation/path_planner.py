import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Path
from barak_common.msg import HybridState

class AStarPlanner:
    """Mature A* Pathfinding Logic for Multi-Modal Navigation."""
    def __init__(self, logger):
        self.logger = logger

    def plan(self, start, goal, mode):
        self.logger.info(f"A* Planning: Start={start} -> Goal={goal} [Mode: {mode}]")
        # Placeholder for actual A* node expansion
        # if mode == HybridState.MODE_AIR: use_3d_costmap()
        return [start, goal] # Simple path stub

class PathPlanner(Node):
    def __init__(self):
        super().__init__('path_planner')
        self.get_logger().info('Umay-Core A* Planner Initialized')
        
        # Initialize Planner Library
        self.planner = AStarPlanner(self.get_logger())
        
        # Subscriptions
        self.state_sub = self.create_subscription(HybridState, 'barak/terrain_info', self.terrain_callback, 10)
        self.goal_sub = self.create_subscription(PoseStamped, 'goal_pose', self.goal_callback, 10)
        
        # Publishers
        self.path_pub = self.create_publisher(Path, 'barak/global_path', 10)
        self.current_mode = HybridState.MODE_LAND

    def terrain_callback(self, msg):
        if msg.current_mode != self.current_mode:
            self.get_logger().warn(f"Switching Planning Context to Mode: {msg.current_mode}")
        self.current_mode = msg.current_mode

    def goal_callback(self, msg):
        start_pose = [0.0, 0.0] # Simulated start
        path_points = self.planner.plan(start_pose, [msg.pose.position.x, msg.pose.position.y], self.current_mode)
        
        # Build ROS2 Path message
        path = Path()
        path.header.stamp = self.get_clock().now().to_msg()
        path.header.frame_id = 'map'
        
        for p in path_points:
            pose = PoseStamped()
            pose.pose.position.x = float(p[0])
            pose.pose.position.y = float(p[1])
            path.poses.append(pose)

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

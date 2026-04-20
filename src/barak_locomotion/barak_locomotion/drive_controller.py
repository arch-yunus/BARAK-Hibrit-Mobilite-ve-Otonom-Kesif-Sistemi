import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from barak_common.msg import HybridState

class DriveController(Node):
    def __init__(self):
        super().__init__('drive_controller')
        self.get_logger().info('Toghrul-Drive Controller Initialized')
        
        # Subscriptions
        self.cmd_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_callback,
            10
        )
        
        self.state_sub = self.create_subscription(
            HybridState,
            'barak/terrain_info',
            self.state_callback,
            10
        )
        
        # Publishers
        self.hybrid_status_pub = self.create_publisher(
            HybridState,
            'barak/current_status',
            10
        )
        
        self.current_mode = HybridState.MODE_LAND
        self.get_logger().info('Default mode: LAND (Tracks active)')

    def state_callback(self, msg):
        if msg.current_mode != self.current_mode:
            self.get_logger().info(f'MODE SWITCH DETECTED: {self.current_mode} -> {msg.current_mode}')
            self.handle_mode_transition(msg.current_mode)
            self.current_mode = msg.current_mode

    def cmd_callback(self, msg):
        # Implementation of multi-modal drive logic
        if self.current_mode == HybridState.MODE_AIR:
            self.get_logger().debug(f'Aerial command: linear={msg.linear.z}, angular={msg.angular.z}')
        elif self.current_mode == HybridState.MODE_WATER:
            self.get_logger().debug(f'Maritime command: surge={msg.linear.x}, yaw={msg.angular.z}')
        else:
            self.get_logger().debug(f'Terrestrial command: v={msg.linear.x}, w={msg.angular.z}')
            
        # Status broadcast
        status = HybridState()
        status.current_mode = self.current_mode
        self.hybrid_status_pub.publish(status)

    def handle_mode_transition(self, target_mode):
        # Logic to activate/deactivate propellers or tracks
        if target_mode == HybridState.MODE_AIR:
            self.get_logger().warn('DEPLOYING PROPELLERS - PREPARING FOR VTOL')
        elif target_mode == HybridState.MODE_WATER:
            self.get_logger().warn('SEALING CHASSIS - ENGAGING WATER JETS')
        else:
            self.get_logger().warn('ENGAGING TRACKS - LAND OPERATION READY')

def main(args=None):
    rclpy.init(args=args)
    node = DriveController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node
from barak_common.msg import Telemetry, HybridState
import base64
import hashlib

class SecureTelemetryNode(Node):
    def __init__(self):
        super().__init__('secure_telemetry')
        self.get_logger().info('Secure Telemetry Node Initialized')
        
        # Subscriptions
        self.status_sub = self.create_subscription(
            HybridState,
            'barak/current_status',
            self.status_callback,
            10
        )
        
        # Publishers
        self.secure_pub = self.create_publisher(
            Telemetry,
            'barak/secure_telemetry',
            10
        )
        
        # Placeholder for encryption key
        self.node_id = "BARAK_UNIT_01"
        self.secret_key = "KADIM_ANAHTAR_2026"

    def status_callback(self, msg):
        # Create telemetry payload
        payload = f"MODE:{msg.current_mode}|BAT:{msg.battery_level}|ARMED:{msg.is_armed}"
        
        # Simulated encryption (Placeholder for real AES/RSA)
        encrypted = base64.b64encode(payload.encode()).decode()
        
        # Simulated signing
        signature = hashlib.sha256((encrypted + self.secret_key).encode()).hexdigest()
        
        telemetry_msg = Telemetry()
        telemetry_msg.sender_id = self.node_id
        telemetry_msg.timestamp = str(self.get_clock().now().nanoseconds)
        telemetry_msg.encrypted_payload = encrypted
        telemetry_msg.signature = signature
        
        self.secure_pub.publish(telemetry_msg)
        self.get_logger().debug(f'Secure telemetry sent: {signature[:8]}...')

def main(args=None):
    rclpy.init(args=args)
    node = SecureTelemetryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Control con odometría: dibuja un 2 en el suelo mediante puntos sucesivos."""
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry, Path


def points_digit_2():
    # Arco superior, diagonal y raya inferior; unidades: metros.
    pts = []
    # Inicio: extremo superior izquierdo; primer tramo sube y recorre arco.
    center_x, center_y, radius = 0.0, 0.5, 0.55
    for i in range(31):
        angle = math.pi - math.pi * i / 30
        pts.append((center_x + radius * math.cos(angle) + 0.55, center_y + radius * math.sin(angle) - 0.5))
    # Desde la parte derecha del arco, diagonal descendente izquierda.
    for i in range(1, 31):
        a = i / 30
        pts.append((1.1 - 1.1*a, -1.15*a))
    # Barra inferior, de izquierda a derecha.
    for i in range(1, 31):
        a = i / 30
        pts.append((1.1*a, -1.15))
    return pts


class DibujarDos(Node):
    def __init__(self):
        super().__init__('dibujar_numero_2')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.path_pub = self.create_publisher(Path, '/trayectoria_real', 10)
        self.create_subscription(Odometry, '/odom', self.on_odom, 10)
        self.waypoints = points_digit_2()
        self.index = 0
        self.pose = None
        self.path = Path()
        self.path.header.frame_id = 'odom'
        self.last_path_point = None
        self.finished = False
        self.timer = self.create_timer(0.05, self.step)
        self.get_logger().info('Grupo 2: esperando odometria; dibujaremos el numero 2')

    def on_odom(self, msg):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1-2*(q.y*q.y+q.z*q.z))
        if self.pose is None:
            self.origin = (p.x, p.y, yaw)
        x0, y0, yaw0 = self.origin
        dx, dy = p.x-x0, p.y-y0
        self.pose = (dx*math.cos(yaw0)+dy*math.sin(yaw0),
                     -dx*math.sin(yaw0)+dy*math.cos(yaw0),
                     (yaw-yaw0+math.pi)%(2*math.pi)-math.pi)
        if self.last_path_point is None or math.hypot(p.x-self.last_path_point[0], p.y-self.last_path_point[1]) > 0.02:
            stamp = PoseStamped()
            stamp.header = msg.header
            stamp.header.frame_id = 'odom'
            stamp.pose = msg.pose.pose
            self.path.poses.append(stamp)
            self.last_path_point = (p.x, p.y)
            self.path.header.stamp = msg.header.stamp
            self.path_pub.publish(self.path)

    def step(self):
        cmd = Twist()
        if self.pose is None or self.finished:
            self.pub.publish(cmd)
            return
        x, y, yaw = self.pose
        while self.index < len(self.waypoints):
            tx, ty = self.waypoints[self.index]
            if math.hypot(tx-x,ty-y) > 0.07:
                break
            self.index += 1
        if self.index >= len(self.waypoints):
            self.finished = True
            self.get_logger().info('Trayectoria del numero 2 completada')
            self.pub.publish(cmd)
            return
        tx, ty = self.waypoints[self.index]
        distance = math.hypot(tx-x,ty-y)
        desired = math.atan2(ty-y,tx-x)
        error = (desired-yaw+math.pi)%(2*math.pi)-math.pi
        cmd.angular.z = max(-1.2,min(1.2, 2.7*error))
        cmd.linear.x = min(0.20, 0.8*distance) if abs(error)<0.7 else 0.0
        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = DibujarDos()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

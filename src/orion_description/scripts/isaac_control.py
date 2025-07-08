import rclpy
from omni.isaac.core.articulations import ArticulationView
from omni.isaac.core.utils.prims import get_prim_at_path
import numpy as np
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
import asyncio

class CygnusController:
    def __init__(self, robot_prim_path):
        # ROS 2 노드 초기화
        if not rclpy.ok():
            rclpy.init()
        self.node = rclpy.create_node('isaac_cygnus_controller')

        # 로봇의 관절을 제어하기 위한 ArticulationView 설정
        self.robot_prim = get_prim_at_path(robot_prim_path)
        self.robot_view = ArticulationView(prim_paths_expr=robot_prim_path, name="robot_view")

        # 제어할 조인트 이름 (URDF 순서와 동일하게)
        self.drive_joint_names = [
            "joint_track_front_left", "joint_track_back_left",
            "joint_track_front_right", "joint_track_back_right"
        ]
        self.flipper_joint_names = [
            "joint_flipper_angle_front_left", "joint_flipper_angle_back_left",
            "joint_flipper_angle_front_right", "joint_flipper_angle_back_right"
        ]
        self.all_joint_names = self.flipper_joint_names + self.drive_joint_names

        # ArticulationView에 조인트 등록
        self.robot_view.initialize()

        # ROS 2 퍼블리셔와 서브스크라이버 생성
        self.cmd_vel_sub = self.node.create_subscription(
            Float64MultiArray,
            '/cygnus/cmd_vel',  # 이 토픽으로 속도 명령을 받음
            self.cmd_vel_callback,
            10)

        self.joint_state_pub = self.node.create_publisher(JointState, '/joint_states', 10)

        self.node.get_logger().info("Isaac Sim Cygnus Controller is ready.")

    def start_ros_spin(self):
        # 비동기적으로 ROS 노드를 실행
        self.ros_task = asyncio.ensure_future(self.spin_ros_node())

    async def spin_ros_node(self):
        while rclpy.ok():
            rclpy.spin_once(self.node, timeout_sec=0.01)
            await asyncio.sleep(0.01)

    def cmd_vel_callback(self, msg: Float64MultiArray):
        # 받은 속도 명령을 시뮬레이션 조인트에 직접 적용
        # [FL, BL, FR, BR] 순서로 명령을 받음
        velocities = np.zeros(8) # 8개 조인트 모두에 대한 배열
        velocities[4] = msg.data[0] # joint_track_front_left
        velocities[5] = msg.data[1] # joint_track_back_left
        velocities[6] = msg.data[2] # joint_track_front_right
        velocities[7] = msg.data[3] # joint_track_back_right
        self.robot_view.set_joint_velocity_targets(velocities)

    def publish_joint_states(self):
        # 현재 조인트 상태를 읽어서 /joint_states 토픽으로 발행
        joint_positions = self.robot_view.get_joint_positions()
        joint_velocities = self.robot_view.get_joint_velocities()

        if joint_positions is not None and joint_velocities is not None:
            msg = JointState()
            msg.header.stamp = self.node.get_clock().now().to_msg()
            msg.name = self.all_joint_names
            msg.position = joint_positions.tolist()
            msg.velocity = joint_velocities.tolist()
            self.joint_state_pub.publish(msg)

# 로봇의 prim 경로 (Stage 탭에서 확인 가능)
ROBOT_PRIM_PATH = "/World/cygnus" 

# 컨트롤러 인스턴스 생성 및 ROS 스핀 시작
controller = CygnusController(ROBOT_PRIM_PATH)
controller.start_ros_spin()

# Isaac Sim의 물리 스텝마다 joint_states를 발행하도록 콜백 등록
from omni.physx.scripts.physicsUtils import add_physics_callback
add_physics_callback("publish_joint_states", controller.publish_joint_states)
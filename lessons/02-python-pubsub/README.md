# 02 · Python으로 publisher/subscriber 만들기

작성자: 조연우 · yencho929@snu.ac.kr

[01 환경 준비](../01-basics/README.md)를 완료하고 Ubuntu22.04/Humble/systemPython3.10에서 실행합니다. 실물 로봇·GUI·GPU는 필요 없습니다. Repository에 완성된 ament_python package가 포함되어 있습니다.

## Class를 Node로 사용하기

Class는 객체의 속성과 동작을 정의합니다. `Talker(Node)`는 ROS Node를 상속하고 `super().__init__('meroedu_talker')`로 node 이름을 등록합니다. `self.count`는 그 instance의 상태, `self.publish_message`는 callback 함수입니다. `String()`은 ROS message 객체이고 실제 문자열은 `msg.data`에 넣습니다.

## 포함된 코드

```
ros_ws/src/meroedu_ros_basics/
  package.xml                    # rclpy/std_msgs 의존성
  setup.py                       # talker/listener 실행 entry point
  setup.cfg                      # ros2 run이 찾는 lib 경로
  resource/meroedu_ros_basics     # ament package 등록 marker
  meroedu_ros_basics/
    __init__.py
    talker.py                    # 1초마다 문자열 발행
    listener.py                  # 수신 callback에서 출력
```

Publisher는 `create_publisher(String, '/meroedu/chatter', 10)`으로 통로를 만들고 `create_timer(1.0, self.publish_message)`로 1초마다 callback을 예약합니다. Callback은 `String()`을 만들고 `msg.data`를 채워 `publish(msg)`로 보냅니다. Count는 메시지마다 증가합니다.

Subscriber는 같은 type/topic으로 `create_subscription(String, '/meroedu/chatter', self.receive, 10)`을 만듭니다. Message가 도착하면 executor가 `receive(msg)`를 실행합니다. Queue depth 10은 모든 기록을 저장한다는 뜻이 아닙니다. 데이터 속도와 처리 속도에 맞게 QoS를 정해야 합니다.

`rclpy.init()`으로 ROS context를 준비하고 node를 생성한 다음 `rclpy.spin(node)`이 timer/수신 callback을 처리합니다. Ctrl+C로 나가면 finally에서 destroy_node와 shutdown을 실행합니다. Callback에서 강제로 sys.exit하지 않습니다. 긴 처리나 sleep을 callback 안에 넣으면 다른 작업도 지연될 수 있습니다.

## Build

```bash
git clone https://github.com/merosnurobotics/meroedu-ros.git
cd meroedu-ros/lessons/02-python-pubsub/ros_ws
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
colcon build --symlink-install --packages-select meroedu_ros_basics
source install/setup.bash
ros2 pkg executables meroedu_ros_basics
```

실행 항목 talker/listener가 표시되어야 합니다. 기존 ROS underlay와 교육 workspace overlay를 차례대로 source합니다. `colcon`은 workspace root인 ros_ws에서 실행합니다. build/install/log는 생성물이며 Git에는 올리지 않습니다.

## 세 터미널 실행

A에서:

```bash
ros2 run meroedu_ros_basics talker
```

B를 **같은 ros_ws 폴더**에서 열고:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=42
ros2 run meroedu_ros_basics listener
```

C는 ROS 설치만 source하면 CLI로 볼 수 있습니다:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
ros2 topic echo /meroedu/chatter std_msgs/msg/String
ros2 topic info /meroedu/chatter --verbose
```

C의 echo를 Ctrl+C로 끝낸 뒤 info 명령을 실행하세요. A는 TX: hello MERO 0, 1, 2…, B는 RX: hello MERO …를 출력합니다. 늦게 켠 listener는 과거 메시지를 모두 받지 않으며 처음 본 count가 0이 아닐 수 있습니다.

## 직접 바꿔보기

1. Talker timer를 1.0→0.5로 바꾸고 다시 실행해 주기를 관찰합니다. Python 코드는 symlink-install이라 재실행으로 반영됩니다. 실행 중인 node에는 자동 적용되지 않습니다.
2. Publisher topic만 /meroedu/other로 바꾸면 listener가 받지 못합니다. 둘의 topic을 맞추면 다시 연결됩니다.
3. setup.py의 entry point·package.xml을 바꿨다면 colcon build와 overlay source를 다시 합니다.

실행 명령에 remap을 줄 수도 있습니다:

```bash
ros2 run meroedu_ros_basics talker --ros-args -r /meroedu/chatter:=/meroedu/other
ros2 run meroedu_ros_basics listener --ros-args -r /meroedu/chatter:=/meroedu/other
```

각 명령은 서로 다른 터미널에서 실행하세요. 원래 talker/listener는 종료해서 이름·publisher가 중복되지 않게 합니다.

## 로봇 강의로 이어가기

String 연습에서 익힌 publish/subscribe 구조는 `/cmd_vel` Twist와 localization PoseStamped에도 적용됩니다. 메시지 의미·단위·frame·timestamp는 각 강의의 계약을 따르세요. [Control](https://mero-website-one.vercel.app/education/control)과 [Localization](https://mero-website-one.vercel.app/education/localization)에서 하드웨어 연결과 위치 feedback을 이어서 배울 수 있습니다.

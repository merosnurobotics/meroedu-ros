# 01 · ROS 2 시작하기

작성자: 조연우 · yencho929@snu.ac.kr

ROS는 Ubuntu 위에서 여러 로봇 프로그램의 통신을 연결하는 middleware입니다. OS 자체를 대체하지 않습니다. Camera driver는 image를 보내고 localization node는 위치를 계산하며 motor bridge는 이동 목표를 하드웨어에 전달합니다.

## 환경 준비

[공식 Humble Ubuntu deb 설치](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)를 따라 **Ubuntu22.04**에 `ros-humble-ros-base`를 설치하세요. Windows/macOS 사용자는 먼저 Ubuntu 실습 환경을 준비합니다. OS 버전이 다르면 이 명령을 그대로 적용하지 않습니다.

```bash
sudo apt update
sudo apt install python3-colcon-common-extensions python3-setuptools ros-humble-std-msgs ros-humble-rosbag2
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
ros2 --help
```

모든 터미널에서 source와 domain 설정을 반복합니다. 여러 팀이면 서로 다른 domain(0~101)을 정합니다. ROS 1의 `roscore`, `rostopic`과 혼용하지 않습니다. ROS 2의 discovery는 node 사이에서 이루어지며 기본 통신에 중앙 roscore를 띄우지 않습니다.

## Node / Package / Workspace / Topic

| 용어 | 의미 | 이번 실습 |
| --- | --- | --- |
| Node | 통신 graph에 참여하는 실행 단위. 한 process에 여러 node가 있을 수도 있음 | 명령을 만드는 publisher, 내용을 읽는 subscriber |
| Topic | 이름과 message type으로 정한 발행/구독 통로 | /meroedu/chatter |
| Message | 실제로 보내는 값과 구조 | std_msgs/msg/String의 data |
| Package | 코드·실행 항목·의존성·설정 묶음 | 다음 회차 meroedu_ros_basics |
| Workspace | src package를 모아 build/install하는 작업 폴더 | 다음 회차 ros_ws |

Topic은 데이터 값을 담은 변수나 파일이 아닙니다. Publisher는 message를 발행하고 subscriber는 새 message를 받습니다. 하나의 topic에 여러 publisher/subscriber가 있을 수 있습니다. 이름과 type, QoS, domain이 맞아야 연결됩니다.

## 터미널로 먼저 메시지 보내기

A:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
ros2 topic pub --rate 1 /meroedu/chatter std_msgs/msg/String "{data: 'hello MERO'}"
```

B:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
ros2 topic echo /meroedu/chatter std_msgs/msg/String
```

C:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
ros2 node list
ros2 topic list -t
ros2 topic info /meroedu/chatter --verbose
ros2 interface show std_msgs/msg/String
ros2 topic hz /meroedu/chatter
```

Echo에 data: hello MERO가 나오고 hz에 대략 1Hz가 보여야 합니다. `hz`는 CLI가 관측한 수신 주기라 실시간 성능 보장 수치가 아닙니다. `echo`와 `pub`도 내부적으로 node를 만들어 graph에 나타납니다. 종료는 각 터미널에서 Ctrl+C입니다.

## Topic / Service / Action / Parameter

- Topic: 계속 들어오는 sensor나 상태 stream. Subscriber마다 받을 수 있음.
- Service: 요청 하나에 응답 하나. 예: 설정 조회. 긴 작업의 진행 상황 관리에는 불편함.
- Action: 오래 걸리는 목표·feedback·결과·취소. 예: 목표 위치까지 이동.
- Parameter: Node의 설정값. 지원하는 node에서 조회·변경 가능.

명령 종류를 이름만 보고 선택하지 않습니다. cmd_vel처럼 최신 속도가 계속 필요한 stream과, 완료 확인이 필요한 목표 이동은 계약이 다릅니다.

## Bag으로 녹화하고 재생하기

A publisher를 켜둔 상태에서 **새로운 강의 작업 폴더**의 C:

```bash
mkdir -p bags
ros2 bag record -o bags/chatter-demo /meroedu/chatter
# 몇 초 뒤 Ctrl+C. 녹화 folder 이름을 재사용하지 않습니다.
ros2 bag info bags/chatter-demo
```

A의 live publisher를 **종료한 뒤**, B echo는 켜두고 C에서:

```bash
ros2 bag play bags/chatter-demo
```

B에는 기록된 message가 다시 들어옵니다. Bag은 단순 mp4가 아니라 message·type·시각을 저장합니다. Live publisher와 replay가 동시에 같은 topic을 보내면 입력이 섞입니다. 실제 robot command topic을 재생하면 로봇이 움직일 수 있으므로 이 회차는 문자열 topic만 다룹니다.

## 문제 해결과 다음 회차

`ros2: command not found`: 새 터미널에서 source 확인. Echo가 멈춘 듯 보이면 publisher가 실제 켜져 있는지 확인합니다. Topic 이름·type·domain·네트워크·QoS 순서로 나누어 확인하세요. 서로 다른 컴퓨터는 같은 domain만으로 연결이 보장되지 않습니다. Discovery multicast와 firewall도 영향을 줍니다.

[02 Python pub/sub](../02-python-pubsub/README.md)에서 직접 node를 만들고 package로 실행합니다.

## 공식 ROS 예제 사용

```bash
sudo apt install ros-humble-demo-nodes-cpp ros-humble-turtlesim
# 같은 source와 ROS_DOMAIN_ID로 각각 다른 터미널에서
ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_cpp listener
```

이 공식 예제는 /chatter topic을 사용합니다. GUI desktop에서는 두 터미널에 `ros2 run turtlesim turtlesim_node`, `ros2 run turtlesim turtle_teleop_key`를 실행하고 두 번째 터미널에 focus를 두어 방향키로 조작합니다. 세 번째 터미널의 `ros2 topic echo /turtle1/cmd_vel geometry_msgs/msg/Twist`로 키 입력이 이동 메시지가 되는 것을 확인하세요.

[공식 설치 예제](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html#try-some-examples) · [공식 turtlesim](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html).

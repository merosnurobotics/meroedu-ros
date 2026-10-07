# 03 · rosbag과 RViz로 데이터 다시 보기

작성자: 조연우 · yencho929@snu.ac.kr

ROS 2 Humble / Ubuntu22.04 / Python3.10 기준. Topic과 메시지는 [01](../01-basics/README.md)에서 먼저 익힙니다. **rosbag2는 message를 시각과 함께 기록/재생**, **RViz는 ROS message를 공간에 표시**하는 도구입니다. RViz는 물리 simulation이나 로봇 위치 계산기가 아닙니다.

## 환경

```bash
sudo apt update
sudo apt install ros-humble-rosbag2 ros-humble-rviz2 ros-humble-geometry-msgs
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
```

Bag은 Jetson에서도 GUI 없이 쓸 수 있습니다. RViz는 GUI/display와 그래픽 환경이 필요합니다. 가능하면 ROS가 준비된 Ubuntu 로컬 컴퓨터에서 실행합니다. Jetson에서 GUI를 원격으로 볼 때는 desktop 세션에 RustDesk로 접속할 수 있습니다. SSH/Tailscale 연결 자체가 GUI·ROS discovery를 보장하지 않습니다. 다른 컴퓨터의 topic을 바로 볼 때는 같은 domain, 네트워크/discovery/firewall을 맞춰야 합니다. 첫 실습은 모든 node를 같은 Ubuntu에서 실행하세요.

## 1. 표시할 pose 발행

교육 저장소를 clone한 뒤 `lessons/03-bag-rviz`에서:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
/usr/bin/python3 pose_publisher.py
```

별도 터미널에서 같은 환경을 source하고:

```bash
ros2 topic echo /meroedu/pose geometry_msgs/msg/PoseStamped --once
```

header.frame_id=map, position=(1.0,0.5,0), orientation.z≈0.38268,w≈0.92388이 나옵니다. yaw 45°를 quaternion으로 표현했습니다. 이 데이터는 형식·화면 실습용이며 실제 센서 localization이 아닙니다. 10Hz로 같은 pose를 새 timestamp와 함께 발행합니다.

## 2. RViz로 pose 보기

같은 강의 폴더의 새 GUI 터미널에서:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
rviz2 -d pose.rviz
```

직접 설정하려면 Fixed Frame=map, Add→By display type→Pose, Topic=/meroedu/pose를 선택합니다. Grid는 길이 눈금, arrow는 위치·방향입니다. Fixed Frame은 화면의 좌표 기준입니다. 이 예제의 pose는 이미 map frame이므로 별도 TF가 필요하지 않습니다. 다른 frame의 센서를 map에서 보려면 촬영/측정 시각의 TF transform이 있어야 합니다.

| 표시 자료 | RViz display | 예시 |
| --- | --- | --- |
| PoseStamped | Pose | 위치와 방향 arrow |
| LaserScan | LaserScan | LiDAR의 거리 점들 |
| PointCloud2 | PointCloud2 | 3D points |
| OccupancyGrid | Map | 지도 cell |
| Image | Image | Camera image |
| TF transform | TF | frame 간 관계 |

RViz가 arrow를 그려준다고 위치 추정이 정확한 것은 아닙니다. 실제로 받은 message의 해석을 돕는 도구입니다.

## 3. Bag으로 기록

Publisher를 켜둔 채 강의 폴더의 새 터미널에서:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=42
mkdir -p bags
ros2 bag record -o bags/pose-demo /meroedu/pose
# 5초 정도 뒤 Ctrl+C
ros2 bag info bags/pose-demo
```

결과는 metadata와 storage file이 들어 있는 폴더입니다. Humble 기본 storage는 SQLite3 .db3입니다. 이름·type·message count·duration을 info로 확인합니다. rosbag CLI 명령은 `ros2 bag`이며, 녹화 폴더를 mp4처럼 취급하지 않습니다. 이미 존재하는 출력 이름은 새 이름으로 바꾸세요. Bags는 Git에 올리지 않습니다.

## 4. 재생

Live publisher를 먼저 Ctrl+C로 끄고 RViz는 열어둡니다:

```bash
ros2 bag play bags/pose-demo
```

원래 topic 이름으로 녹화된 message가 다시 발행되어 같은 arrow를 볼 수 있습니다. Live publisher가 같이 켜져 있으면 두 입력이 섞입니다. 반복 재생은 `--loop`, 느리게 재생은 `--rate 0.5`를 사용할 수 있습니다. 실제 motor command bag은 hardware subscriber가 있으면 움직임을 유발하므로 이 회차는 표시용 pose만 재생합니다.

Timestamp를 이용하는 여러 sensor를 재생할 때는 ROS time을 맞춰야 합니다:

```bash
ros2 bag play bags/pose-demo --clock
# RViz를 bag 재생 시각에 맞출 경우 별도 터미널에서
rviz2 -d pose.rviz --ros-args -p use_sim_time:=true
```

`--clock`은 /clock을 발행하고 `use_sim_time=true`인 node가 그 시간을 쓰게 합니다. /clock이 없는데 true로 설정하면 시간이 진행하지 않을 수 있습니다. /tf·/tf_static이 필요한 데이터는 관련 transform도 기록해야 합니다. 첫 예제는 map에 직접 쓰인 pose라 TF 없이 확인됩니다.

## 문제 확인

- No messages: publisher 또는 replay가 켜져 있는지 topic echo로 확인.
- Fixed Frame error: frame 이름·TF 경로·timestamp 확인.
- QoS mismatch: `ros2 topic info /topic --verbose`, sensor best-effort/reliable 설정 확인.
- ROS는 되는데 GUI가 안 뜸: desktop session / DISPLAY / graphics 확인. SSH shell만으로 화면이 생기지는 않음.

Bag 기록/재생과 pose 발행은 실제 ROS로 확인합니다. RViz config는 pose display가 지정된 준비 파일이며 GUI 동작은 자신의 desktop 환경에서 확인해야 합니다.

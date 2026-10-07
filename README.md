# MERO 교육 · ROS 2

작성자: 조연우 · yencho929@snu.ac.kr

처음 ROS를 사용하는 사람을 위한 Humble 시리즈입니다. Ubuntu 22.04 / ROS 2 Humble / Python 3.10 기준이며 로봇이나 외부 데이터 없이 실행합니다.

| 순서 | 강의 | 실습 | 웹 자료 |
| --- | --- | --- | --- |
| 01 | ROS 2 시작하기 | [lessons/01-basics](lessons/01-basics/README.md) | [사이트](https://mero-website-one.vercel.app/education/ros/basics) |
| 02 | Python publisher/subscriber | [lessons/02-python-pubsub](lessons/02-python-pubsub/README.md) | [사이트](https://mero-website-one.vercel.app/education/ros/python-pubsub) |

| 03 | rosbag과 RViz | [lessons/03-bag-rviz](lessons/03-bag-rviz/README.md) | [사이트](https://mero-website-one.vercel.app/education/ros/bag-rviz) |

```bash
git clone https://github.com/merosnurobotics/meroedu-ros.git
cd meroedu-ros
```

각 강의 README를 따라갑니다. 미래 회차는 lessons에 별도 폴더로 추가하며 기존 경로를 바꾸지 않습니다. 필수 환경 설정과 작은 예제만 담고 PDF 원본·개인 설정·실습 녹화 파일은 포함하지 않습니다. [참고한 자료와 재구성 내용](NOTICE.md) · [Apache-2.0](LICENSE)

## ROS 하드웨어·위치 시리즈

웹사이트의 ROS 분류에는 다음 실습도 모았습니다. 코드는 각각의 경량 교육 저장소에서 실행합니다. 이 저장소의 예제를 복제하거나 원본 로봇 프로젝트를 요구하지 않습니다.

| 강의 | 사이트 | 필요한 실습 코드 |
| --- | --- | --- |
| Localization 결과를 topic으로 발행 | [ROS 강의](https://mero-website-one.vercel.app/education/ros/localization-topics) | [meroedu-localization / 02](https://github.com/merosnurobotics/meroedu-localization/tree/main/lessons/02-ros2-topics) |
| ROS → Arduino encoder motor | [ROS 강의](https://mero-website-one.vercel.app/education/ros/arduino-motor) | [meroedu-control / 02](https://github.com/merosnurobotics/meroedu-control/tree/main/lessons/02-ros-arduino-motor) |
| ROS → OpenRB DYNAMIXEL | [ROS 강의](https://mero-website-one.vercel.app/education/ros/dynamixel) | [meroedu-control / 04](https://github.com/merosnurobotics/meroedu-control/tree/main/lessons/04-ros2-dynamixel) |

검증(2026-10-08): colcon build, 실제 ROS talker/listener, PoseStamped 31개 bag record와 replay→echo를 확인했습니다. 공식 demo_nodes_cpp talker/listener 통신도 확인했습니다. Turtlesim GUI 및 RViz desktop 표시는 별도 환경에서 확인해야 합니다. ROS package는 Ubuntu22.04/Humble/systemPython3.10 기준입니다.

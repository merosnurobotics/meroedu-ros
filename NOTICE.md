# 출처와 재구성

작성: MERO 교육 · 조연우 · yencho929@snu.ac.kr · 2026-10-08

사용자가 제공한 `[강의] ROS 강의자료 (전체).pdf` (43쪽, 기계시스템설계 로봇프로그래밍 기초 ROS)의 개념과 교육 순서를 참고했습니다. 저자 정보는 파일에 별도로 확인되지 않았습니다. PDF 전체·슬라이드 이미지는 재배포하지 않습니다.

- pp.2–10: OS와 ROS의 역할, sensor data와 bag 재생
- pp.13–14: package, node, topic
- pp.16–19: Python class와 inheritance
- pp.21–29: publisher, Node 초기화, timer와 message
- pp.31–40: subscriber, callback, spin과 종료

Foxy/Elice 환경·미완성 TODO 코드는 Ubuntu22.04/Humble 기준의 독립 실행 예제로 새로 정리했습니다. 직접 sys.exit로 callback을 종료하는 대신 Ctrl+C와 finally에서 node/context를 정리합니다. 도식은 웹사이트에서 HTML/CSS로 작성했습니다.

공식 ROS 2 Humble documentation 및 Apache-2.0 ROS 2 examples의 공개 교육 패턴을 참고했습니다:
- https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html
- https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html
- https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html
- https://github.com/ros2/examples/tree/humble/rclpy/topics

ROS 2 examples: Copyright 2016 Open Source Robotics Foundation, Inc. Apache License, Version 2.0. 원본은 AS IS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND 조건으로 배포됩니다. 교육용 node는 topic/name/timer 및 종료 처리를 재구성했습니다.

예제 코드는 Apache-2.0입니다. PDF 원자료의 권리는 원저작자에게 있습니다. ROS 예제와 본 자료는 특정 하드웨어 동작을 검증하는 코드가 아닙니다.

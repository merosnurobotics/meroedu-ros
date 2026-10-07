from setuptools import setup
name = 'meroedu_ros_basics'
setup(name=name, version='0.1.0', packages=[name],
 data_files=[('share/ament_index/resource_index/packages', ['resource/'+name]),
             ('share/'+name, ['package.xml'])],
 install_requires=['setuptools'], zip_safe=True,
 maintainer='MERO / 조연우', maintainer_email='yencho929@snu.ac.kr',
 description='MERO ROS 2 beginner publisher and subscriber', license='Apache-2.0',
 entry_points={'console_scripts': ['talker = meroedu_ros_basics.talker:main',
                                  'listener = meroedu_ros_basics.listener:main']})

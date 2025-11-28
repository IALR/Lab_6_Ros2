cmake_minimum_required(VERSION 3.8)
project(robot_actions)

# This package uses Python
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(custom_interfaces REQUIRED)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install executables (console scripts from setup.py)
install(
  PROGRAMS
    robot_actions/battery_charger.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

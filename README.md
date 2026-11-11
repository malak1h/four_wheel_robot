# four_wheel_robot

Four-wheel skid-steer robot for ROS 2 Humble and Gazebo Classic, with a 2D lidar, ros2_control and an 8x8 m test room.

## Run
    colcon build --symlink-install --packages-select four_wheel_robot
    source install/setup.bash
    ros2 launch four_wheel_robot gazebo.launch.py
    ros2 launch four_wheel_robot rviz.launch.py
    ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/diff_drive_controller/cmd_vel_unstamped

If Gazebo shows an empty world, run `killall -9 gzserver gzclient` and relaunch.

## Known issues
- Forward and backward driving works. Turning with j/l in teleop is unreliable. Wheel friction (mu1/mu2/fdir1 in the xacro) probably needs tuning.
- RViz config is untested.

## Next
- Fix turning, add a camera, then SLAM (slam_toolbox) and Nav2.

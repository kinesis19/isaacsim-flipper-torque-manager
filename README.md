# isaacsim-flipper-torque-manager
## Description
![isaac_ros_control_Mobile Base with 4 flipper Model_gif](/README_Resources/isaacsim_mobilebase_gif.gif)

This is a simulation package that works by importing a **Mobile Base with 4 flipper** into Isaac Sim and synchronizing motion planning in RViz to Isaac-Sim. The package allows for seamless integration and control of the **Mobile Base with 4 flipper** in a simulated environment.

## Table of Contents
- [Built With](#built-with)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Preview](#preview)
- [How to Run Mobile Base with 4 flipper Model](#how-to-run-Mobile Base with 4 flipper Model)
- [License](#license)
- [Team Members](#team-members)
- [Contact](#contact)

## Built With
- **Mobile Base with 4 flipper Model**
    - URDF: Converted the Mobile Base with 4 flipper model to a URDF file that can be controlled in simulation.
- **Simulation**
    - Isaac Sim: For simulation of the Mobile Base with 4 flipper Model.
- **Framework**
    - ROS2: To synchronize the Mobile Base with 4 flipper Model on RViz with the Mobile Base with 4 flipper Model on Isaac Sim.

## Prerequisites
- **Hardware Requirements**
    - Not yet (Digital Twin is not already available)
- **Software Requirements**
    - ROS2 (Humble)
    - Ubuntu 22.04
    - Isaac Sim 4.5.0 (Humble)
    - RViz (Humble)

## Installation
1. **Clone the repository:**
    ```bash
    cd {workspace}
    git clone https://github.com/kinesis19/isaacsim-flipper-torque-manager.git
    cd isaacsim-flipper-torque-manager
    ```

2. **Install Dependencies:**
    ```bash
    sudo apt update
    xargs -a dependencies.txt sudo apt install
    ```

3. **Build the package:**
    ```bash
    colcon build
    ```

4. **Source the workspace:**
    ```bash
    source ~/{workspace name}/isaacsim-flipper-torque-manager/install/setup.bash
    ```

## Usage
1. **Run the package:**
    ```bash
    ros2 launch cygnus_moveit_config demo.launch.py
    ```

## Preview


## How to run this package
To run the **Mobile Base with 4 flipper** in the simulation environment, follow these steps:

1. **Set ROS DOMAIN ID:**
    - Ensure that the ROS DOMAIN ID is set to 0. If you need to change it, update the DOMAIN ID in the Isaac Sim Action Graph and the ROS2 environment.
    ```bash
    vim ~/.bashrc # You can use anything else.
    export ROS_DOMAIN_ID=19
    ```
2. **Launch Isaac Sim:**
    - Open Isaac Sim and load the **MainScene.usd** file.
    ![img1](/README_Resources/img1.png)

3. **Start ROS2:**
    - Ensure that ROS2 is properly sourced and running.
    ![img2](/README_Resources/img2.png)

4. **Run the Motion Planning Node:**
    - Execute the following command to start the motion planning node:
    ```bash
    ros2 launch cygnus_moveit_config demo.launch.py
    ```
    ![img3](/README_Resources/img3.png)

5. **Set Motion Position in RViz:**
    - Open RViz and set the desired motion planning pose.
    - The **Mobile Base with 4 flipper** in Isaac Sim and RViz will move to the pose set by the User.
    ![img4](/README_Resources/img4.png)

## License
This project is licensed under the MIT License.

## Developer
#### Develop this package
- 19th Kinesis <a href="https://github.com/kinesis19"><img src="https://img.shields.io/badge/GitHub-gray?style=flat&logo=github&logoColor=white"/></a>

## Contact
For any questions or support, please contact us at [linkdin](https://www.linkedin.com/in/kinesis19/) or <kinesis@kashic.dev>.

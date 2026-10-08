#include <rclcpp/rclcpp.hpp>
#include <chrono>
#include <exception>
#include <thread>

#include <ego_planner/ego_replan_fsm.h>

using namespace ego_planner;

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("ego_planner_node");

    EGOReplanFSM rebo_replan;

    rebo_replan.init(node);

    // A mapping/planning callback can throw on an invalid raycast or trajectory.
    // Keep the node available for the next goal and record the actual exception.
    while (rclcpp::ok())
    {
        try
        {
            rclcpp::spin(node);
            break;
        }
        catch (const std::exception& error)
        {
            RCLCPP_ERROR(node->get_logger(), "Planner callback failed: %s", error.what());
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }
    rclcpp::shutdown();

    return 0;
}

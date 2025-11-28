#!/usr/bin/env python3
"""
Battery Charging Action Server
================================
Simulates a robot battery charging station.
"""

import time
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from custom_interfaces.action import ChargeBattery


class BatteryCharger(Node):
    """
    The charging station that handles incoming charge requests.
    """

    def __init__(self):
        super().__init__('battery_charger')
        
        # Starting battery level
        self.current_battery = 20  # Start low (20%)

        # How fast we charge (% per second)
        self.charge_rate = 5.0

        self.get_logger().info('=================================')
        self.get_logger().info('🔋 Battery Charging Station Ready')
        self.get_logger().info(f'   Current battery: {self.current_battery}%')
        self.get_logger().info(f'   Charge rate: {self.charge_rate}%/sec')
        self.get_logger().info('=================================')

        # Create the action server
        self.action_server = ActionServer(
            self,
            ChargeBattery,
            'charge_battery',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

    # -----------------------------------------------
    # Goal callback
    # -----------------------------------------------
    def goal_callback(self, goal_request):
        """
        Called when someone requests charging.
        Decide: accept or reject
        """
        target = goal_request.target_percentage
        self.get_logger().info(f'📥 Charging request received: {target}%')
        
        # Validation: Is target valid?
        if target < 0 or target > 100:
            self.get_logger().warn(f'❌ Invalid target: {target}%')
            return GoalResponse.REJECT
        
        # Validation: Already charged enough?
        if self.current_battery >= target:
            self.get_logger().warn(
                f'❌ Already at {self.current_battery}% '
                f'(target: {target}%)'
            )
            return GoalResponse.REJECT
        
        self.get_logger().info('✅ Goal accepted - Starting charge!')
        return GoalResponse.ACCEPT

    # -----------------------------------------------
    # Cancel callback
    # -----------------------------------------------
    def cancel_callback(self, goal_handle):
        """
        Called when someone wants to cancel charging.
        """
        self.get_logger().info('🛑 Cancel request received')
        return CancelResponse.ACCEPT

    # -----------------------------------------------
    # Execute callback
    # -----------------------------------------------
    def execute_callback(self, goal_handle):
        """
        Main charging logic when goal is accepted.
        """
        self.get_logger().info('⚡ Charging started!')

        # Get target from goal
        target = goal_handle.request.target_percentage

        # Record start time
        start_time = time.time()

        # Feedback message
        feedback_msg = ChargeBattery.Feedback()

        # -----------------------------------------
        # Charging loop
        # -----------------------------------------
        while self.current_battery < target:
            # Check if canceled
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = ChargeBattery.Result()
                result.success = False
                result.final_percentage = int(self.current_battery)
                result.charging_time = time.time() - start_time
                self.get_logger().info('🛑 Charging canceled!')
                return result

            # Charge a bit
            charge_amount = self.charge_rate * 0.5  # 0.5 sec intervals
            self.current_battery = min(self.current_battery + charge_amount, target)

            # Feedback calculation
            remaining_percent = target - self.current_battery
            time_remaining = remaining_percent / self.charge_rate

            feedback_msg.current_percentage = int(self.current_battery)
            feedback_msg.time_remaining = time_remaining
            feedback_msg.charging_rate = self.charge_rate

            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(
                f'🔋 Charging: {feedback_msg.current_percentage}% '
                f'(~{time_remaining:.1f}s left)'
            )

            time.sleep(0.5)

        # Charging complete
        goal_handle.succeed()
        total_time = time.time() - start_time

        result = ChargeBattery.Result()
        result.success = True
        result.final_percentage = int(self.current_battery)
        result.charging_time = total_time

        self.get_logger().info('=================================')
        self.get_logger().info('✅ Charging complete!')
        self.get_logger().info(f'   Final: {result.final_percentage}%')
        self.get_logger().info(f'   Time: {result.charging_time:.1f}s')
        self.get_logger().info('=================================')

        return result


# -----------------------------------------------
# Main entry point
# -----------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    charger = BatteryCharger()
    try:
        rclpy.spin(charger)
    except KeyboardInterrupt:
        charger.get_logger().info('Shutting down...')
    charger.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

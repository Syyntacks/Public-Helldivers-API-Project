from . import datetime_converter



def parse_major_order_data(data, user_timezone="UTC"):
    
    # List to hold multiple dictionaries
    parsed_orders = []
    
    if not isinstance(data, list):
        print(f"Error: Expected a list of major orders, but received {type(data)}")
        return None

    try:
        
        for order in data:
            order_details = {}

            order_details["order_id"] = order.get("id32")

            order_details["order_expires"] = datetime_converter.get_expiration_from_seconds(order.get("expiresIn"), user_timezone)

            # Mission settings
            mission_settings = order.get("setting", {})
            order_details["order_type"] = mission_settings.get("type")
            order_details["order_title"] = mission_settings.get("overrideTitle")
            order_details["order_briefing"] = mission_settings.get("overrideBrief")
            order_details["order_taskDescr"] = mission_settings.get("taskDescription")

            # Task-specifics
            tasks_list = mission_settings.get("tasks", [])
                # Progress
            order_progress = order.get("progress")
            order_details["order_progress"] = order_progress
            parsed_tasks = [] # Holds parsed tasks

            for i, task in enumerate(tasks_list): # Enumerate turns a number into an index for a list
                task_details = {}
                values = task.get("values", [])
                valueTypes = task.get("valueTypes", [])
                value_map = dict(zip(valueTypes, values)) # Pair two value lists together

                task_details["goal"] = value_map.get(3) # 3 = goal
                task_details["target_planet_id"] = value_map.get(12) # 12 = Planet ID for MO
                
                if task.get("type") == 2:
                    task_details["type"] = "Collection task"
                elif task.get("type") == 4:
                    task_details["type"] = f"Defend against {task_details["goal"]}"
                elif task.get("type") == 12 or 13:
                    task_details["type"] = "Defense task"
                else:
                    task_details["type"] = task.get("type")
                

                if i < len(tasks_list):
                    task_details["progress"] = order_progress[i]
                else:
                    task_details["progress"] = 0 # If no progress data available

                parsed_tasks.append(task_details)

            order_details["tasks"] = parsed_tasks

            # Reward Parsing
            reward_data = mission_settings.get("reward")
            if reward_data and isinstance(reward_data, dict):
                order_details["rewards_amount"] = reward_data.get("amount")
            else:
                order_details["rewards_amount"] = None
                

            parsed_orders.append(order_details)

        print(f"Successfully parsed {len(parsed_orders)} major orders.")
        return parsed_orders
            
    except (AttributeError, TypeError) as e:
        print (f"Error processing major order's data: {e}")
        return None
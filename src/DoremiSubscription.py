from src.constants import MUSIC_PLANS, VIDEO_PLANS, PODCAST_PLANS, TOPUP_PLANS
from src.enums import ECommands
from src.helpers import is_command_valid, is_plan_valid, is_category_valid, is_date_valid, is_topup_valid, \
    increment_and_subtract_date


class DoremiSubscription:
    __subscription: dict

    def __init__(self):
        # format for subscription
        # {"subs": [("MUSIC","PREMIUM" 3)], "topups: [("TEN_DEVICE",1)], "start_date": "DD-MM-YYYY",
        # renewal_date: "DD-MM-YYYY"}
        self.__subscription = {}

    def __invoke_command_method(self, command: ECommands, *args):
        """
        Checks and performs a command provided
        """
        if command == ECommands.START_SUBSCRIPTION:
            subs_date = args[0]
            if is_date_valid(subs_date):
                self.__subscription["start_date"] = subs_date
                self.__subscription["subs"] = []
                self.__subscription["topups"] = []
                return True
            else:
                return "ADD_SUBSCRIPTION_FAILED INVALID_DATE"

        elif command == ECommands.ADD_SUBSCRIPTION:
            if self.__subscription:
                subscription_category = args[0]
                plan_name = args[1]

                # check if plan and category are valid or not
                if is_plan_valid(plan_name) and is_category_valid(subscription_category):
                    # check if category is already present
                    for subs in self.__subscription["subs"]:
                        if subscription_category == subs[0]:
                            return "ADD_SUBSCRIPTION_FAILED DUPLICATE_CATEGORY"

                    self.__subscription["subs"].append((args[0], args[1]))
                    return True
            return "SUBSCRIPTIONS_NOT_FOUND"

        elif command == ECommands.ADD_TOPUP:
            if self.__subscription and self.__subscription["subs"]:
                topup_name = args[0]

                # check if plan and category are valid or not
                if is_topup_valid(topup_name):
                    # check if category is already present
                    for topups in self.__subscription["topups"]:
                        if topup_name == topups[0]:
                            return "ADD_TOPUP_FAILED DUPLICATE_TOPUP"

                    self.__subscription["topups"].append((args[0], int(args[1])))
                    return True
            return "SUBSCRIPTIONS_NOT_FOUND"

        elif command == ECommands.PRINT_RENEWAL_DETAILS:
            if self.__subscription:
                renewal_cost = 0
                return_data = []
                # get subscriptions costing and renewal date
                for subs in self.__subscription["subs"]:
                    category_name = subs[0]
                    plan_name = subs[1]
                    # get costing
                    plan_data = []
                    if category_name == "MUSIC":
                        plan_data = MUSIC_PLANS

                    if category_name == "VIDEO":
                        plan_data = VIDEO_PLANS

                    if category_name == "PODCAST":
                        plan_data = PODCAST_PLANS

                    for plan in plan_data:
                        if plan["name"] == plan_name:
                            # get renewal date based on plan_name
                            renewal_date = increment_and_subtract_date(self.__subscription["start_date"],
                                                                       plan["month"], 10)
                            renewal_cost += plan["cost"]
                            return_data.append(f"RENEWAL_REMINDER {category_name} {renewal_date}")
                            break

                # get topups costings
                for topup in self.__subscription["topups"]:
                    topup_name = topup[0]
                    topup_months = topup[1]

                    for topup_data in TOPUP_PLANS:
                        if topup_data["name"] == topup_name:
                            renewal_cost += topup_data["cost"] * topup_months
                            break

                return_data.append(f"RENEWAL_AMOUNT {renewal_cost}")

                return return_data

            return "SUBSCRIPTIONS_NOT_FOUND"

        return "None"

    def run_command(self, command: str, *args):
        """
        Takes and run command with provided arguments
        Args:
            command: String
            *args: List of arguments required by the command

        Returns:
            str: Result of the command
        """
        if is_command_valid(command):
            invoke_result = self.__invoke_command_method(ECommands(command), *args)

            if invoke_result == "None":
                # no command was invoked
                return "INVALID_COMMAND"
            else:
                return invoke_result
        else:
            return "INVALID_COMMAND"

from enum import Enum


class ECommands(Enum):
    START_SUBSCRIPTION = "START_SUBSCRIPTION"
    ADD_SUBSCRIPTION = "ADD_SUBSCRIPTION"
    ADD_TOPUP = "ADD_TOPUP"
    PRINT_RENEWAL_DETAILS = "PRINT_RENEWAL_DETAILS"

    @classmethod
    def has_command(cls, value):
        return any(value == item.value for item in cls)


class EInfo(Enum):
    RENEWAL_AMOUNT = "RENEWAL_AMOUNT"
    RENEWAL_DATE = "RENEWAL_DATE"
    RENEWAL_REMINDER = "RENEWAL_REMINDER"


class EErrorInfo(Enum):
    DUPLICATE_CATEGORY = "DUPLICATE_CATEGORY"
    DUPLICATE_TOPUP = "DUPLICATE_TOPUP"
    INVALID_DATE = "INVALID_DATE"

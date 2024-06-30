import os
import json
import lambda_entry_point
import console_esm_simulator

CHAT_ID = 451578667

def main():
    aws_event = console_esm_simulator.get_aws_event(CHAT_ID, "/start", user_nick="user321")
    print(json.dumps(aws_event))

    lambda_result = lambda_entry_point.lambda_handler(aws_event, {})
    print(json.dumps(lambda_result))


if __name__ == "__main__":
    main()


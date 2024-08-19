def store_in_dynamodb():
    print("do something")


def consume_sqs_message():
    store_in_dynamodb()


def main():
    consume_sqs_message()


if __name__ == '__main__':
    main()
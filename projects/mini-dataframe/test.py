from pprint import pprint

from mini_dataframe import MiniDataFrame


# Sample data
users = MiniDataFrame(
    {
        "user_id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "age": [25, 30, 35, 40],
    }
)

orders = MiniDataFrame(
    {
        "order_id": [101, 102, 103, 104, 105],
        "user_id": [2, 1, 3, 1, 5],
        "amount": [250.0, 100.0, 300.0, 150.0, 400.0],
    }
)


def main():
    user_orders = users.join(orders, on="user_id", how="left")
    print("\nUser Orders (Left Join):")
    print(user_orders)

    print("\nUsers older than 30:")
    print(users.query("age > 30"))

    print("\nUser stats:")
    pprint(users.describe())

    extra_users = MiniDataFrame(
        {
            "user_id": [6, 7],
            "name": ["Eve", "Frank"],
            "age": [28, 33],
        }
    )
    all_users = MiniDataFrame.concat([users, extra_users])
    print("\nAll Users (Stacked):")
    print(all_users)

    locations = MiniDataFrame(
        {
            "city": ["NY", "LA", "SF", "NY"],
            "country": ["USA", "USA", "USA", "USA"],
        }
    )
    user_locations = MiniDataFrame.concat(
        [users.iloc(slice(0, 4)), locations], axis=1
    )
    print("\nUsers with location info:")
    print(user_locations)


if __name__ == "__main__":
    main()

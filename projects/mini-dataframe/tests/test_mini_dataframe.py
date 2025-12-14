import pytest

from mini_dataframe import MiniDataFrame


@pytest.fixture
def users():
    return MiniDataFrame(
        {
            "user_id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Charlie", "Diana"],
            "age": [25, 30, 35, 40],
        }
    )


@pytest.fixture
def orders():
    return MiniDataFrame(
        {
            "order_id": [101, 102, 103, 104, 105],
            "user_id": [2, 1, 3, 1, 5],
            "amount": [250.0, 100.0, 300.0, 150.0, 400.0],
        }
    )


def test_shape_and_stats(users):
    assert users.shape() == (4, 3)
    assert users.mean("age") == pytest.approx(32.5)
    assert users.describe()["age"]["max"] == 40


def test_query_and_select(users):
    older = users.query("age > 30")
    assert older.shape() == (2, 3)

    selected = users.select("name", "age", where="age >= 30")
    assert selected.columns == ["name", "age"]
    assert selected["name"] == ["Bob", "Charlie", "Diana"]


def test_join_and_concat(users, orders):
    joined = users.join(orders, on="user_id", how="left")
    assert joined.shape() == (5, 5)

    order_ids = joined["order_id"]
    assert order_ids.count(None) == 1
    assert set(order_ids) >= {101, 102, 103, 104}

    stacked = MiniDataFrame.concat(
        [users.iloc(slice(0, 2)), users.iloc(slice(2, 4))]
    )
    assert stacked["user_id"] == users["user_id"]

    locations = MiniDataFrame({"city": ["NY", "LA", "SF", "NY"]})
    wide = MiniDataFrame.concat([users.iloc(slice(0, 4)), locations], axis=1)
    assert wide.shape() == (4, 4)
    assert wide["city"][0] == "NY"

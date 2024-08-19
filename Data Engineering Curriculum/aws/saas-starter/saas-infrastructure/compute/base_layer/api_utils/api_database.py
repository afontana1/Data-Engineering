import boto3
import os
from api_utils.api_exception import ApiException
from api_utils.api_item import ApiItem


class ApiDatabase:
    def __init__(self, table_name: str):
        self.table_name: str = table_name
        self.table = self._create_table_client(table_name)

    @staticmethod
    def from_env(key: str):
        return ApiDatabase(os.getenv(key, "no_table_specified"))

    def _create_table_client(self, table_name: str):
        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(table_name)
            return table
        except Exception as e:
            raise ApiException(500, f"Unable to connect to table: {e}")

    def put_item(self, api_item: ApiItem):
        return self.table.put_item(Item=api_item.serialize())

    def get_item(self, item: ApiItem):
        return self.get_item_with_keys(item.pk, item.sk)

    def get_item_with_keys(self, pk: str, sk: str):
        response = self.table.get_item(Key={"pk": pk, "sk": sk})
        if "Item" not in response:
            raise ApiException(404, "Item not found in table!")
        return response["Item"]

    def from_index(self, index_name: str, index_pk: str):
        return ApiDatabaseProjection(
            self.table, index_name=index_name, index_pk=index_pk
        )

    def update_item(self, pk: str, sk: str, updated_values: dict):

        expression_attr_values = {}
        expression_keys = []
        i = 1

        for k, v in updated_values.items():
            key_name = f":v{i}"
            expression_keys.append(f"{k} = {key_name}")
            expression_attr_values[key_name] = v
            i += 1

        update_expression_query = "SET " + ", ".join(expression_keys)

        return self.table.update_item(
            Key={"pk": pk, "sk": sk},
            UpdateExpression=update_expression_query,
            ExpressionAttributeValues=expression_attr_values,
        )

    def delete_item(self, item: ApiItem):
        self.delete_item_with_keys(pk=item.pk, sk=item.sk)

    def delete_item_with_keys(self, pk: str, sk: str):
        self.table.delete_item(Key={"pk": pk, "sk": sk})


class ApiDatabaseProjection:
    def __init__(self, table, index_name: str, index_pk: str):
        self.table = table
        self.index_name: str = index_name
        self.index_pk: str = index_pk

    def get_items(
        self, key: str, limit: int = 10, must_exist: bool = True, reverse: bool = False
    ):
        response = self.table.query(
            IndexName=self.index_name,
            KeyConditionExpression="#K = :v1",
            ExpressionAttributeValues={
                ":v1": key,
            },
            ExpressionAttributeNames={
                "#K": self.index_pk,
            },
            Limit=limit,
            ScanIndexForward=not reverse,
        )

        # Look for the item in the response.
        if "Items" not in response:
            raise ApiException(404, "Item key was not found")
        items = response["Items"]

        # If must_exist, then check if there is at least 1 item.
        if len(items) == 0 and must_exist:
            raise ApiException(404, "Item key was not found")

        return items

    def get_item(
        self, key: str, limit: int = 10, must_exist: bool = True, reverse: bool = False
    ):
        items = self.get_items(key, limit=limit, must_exist=must_exist, reverse=reverse)
        return items[0]

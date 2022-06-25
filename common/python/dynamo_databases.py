from json import dumps, loads
from decimal import Decimal

from boto3 import resource
from boto3.dynamodb.conditions import Key

from common.enums import NamingConventions
from common.transform import TransformDictionary

class DynamoDatabase(object):

    def __init__(self, table_name: str, hash_key: str, sort_key: str):
        dynamodb = resource("dynamodb")
        self._table = dynamodb.Table(table_name)
        self._hash_key = hash_key
        self._sort_key = sort_key

    @staticmethod
    def __format_to_dynamo(item: dict) -> dict:
        item = TransformDictionary.update_naming_convention(
            item, 
            current=NamingConventions.SNAKE, 
            new=NamingConventions.PASCAL
        )
        return loads(dumps(item), parse_float=Decimal)

    @staticmethod
    def __format_from_dynamo(item: dict) -> dict:
        return TransformDictionary.update_naming_convention(
            item, 
            current=NamingConventions.PASCAL, 
            new=NamingConventions.SNAKE
        )
    
    def _put(self, items: list = []) -> None:
        def put_item(table, item: dict) -> None:
            table.put_item(Item=self.__format_to_dynamo(item))

        if len(items) == 1:
            put_item(self._table, items.pop())
        else:
            with self._table.batch_writer() as batch:
                for item in items:
                    put_item(batch, item)

    def _query(self, *, hash_key: str = None, sort_key: str = None) -> list[dict]:
        if hash_key is None and sort_key is None:
            raise ValueError("Expected one argument with value different from None.")

        keyConditionExpression = None
        
        if hash_key is not None:
            keyConditionExpression = Key(self._hash_key).eq(hash_key)
        
        if sort_key is not None:
            if keyConditionExpression is not None:
                keyConditionExpression = keyConditionExpression & Key(self._sort_key).eq(sort_key)
            else:
                keyConditionExpression = Key(self._sort_key).eq(sort_key)

        response = self._table.query(KeyConditionExpression=keyConditionExpression)
        print(dumps(response))
        items = response["Items"]

        return [self.__format_from_dynamo(item) for item in items]

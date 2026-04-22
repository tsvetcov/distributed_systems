from dataclasses import dataclass

import asyncpg


@dataclass
class ItemEntry:
    item_id: int
    user_id: int
    title: str
    description: str


class ItemStorage:
    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        # We initialize client here, because we need to connect it,
        # __init__ method doesn't support awaits.
        #
        # Pool will be configured using env variables.
        self._pool = await asyncpg.create_pool()

    async def disconnect(self) -> None:
        # Connections should be gracefully closed on app exit to avoid
        # resource leaks.
        await self._pool.close()

    async def create_tables_structure(self) -> None:
        """
        Создайте таблицу items со следующими колонками:
         item_id (int) - обязательное поле, значения должны быть уникальными
         user_id (int) - обязательное поле
         title (str) - обязательное поле
         description (str) - обязательное поле
        """
        # In production environment we will use migration tool
        # like https://github.com/pressly/goose
        table_creation = """
	    CREATE TABLE items(
	    item_id int PRIMARY KEY,
	    user_id int NOT NULL,
	    title varchar(100) NOT NULL,
        description text);
	    """
	    async with self._pool.acquire() as cur_create:
            await connect.execute(table_creation)

    async def save_items(self, items: list[ItemEntry]) -> None:
        """
        Напишите код для вставки записей в таблицу items одним запросом, цикл
        использовать нельзя.
        """
        # Don't use str-formatting, query args should be escaped to avoid
        # sql injections https://habr.com/ru/articles/148151/.
        insert_into_table = """
	INSERT INTO items (item_id, user_id, title, description) VALUES ($1, $2, $3, $4);
	"""
        input = [(enrty.item_id, entry.user_id, entry.title, entry.description) for entry in items]
	    async with self._pool.acquire() as cur_insert:
            await connect.executemany(insert_into_table, input)

    async def find_similar_items(
        self, user_id: int, title: str, description: str
    ) -> list[ItemEntry]:
        """
        Напишите код для поиска записей, имеющих указанные user_id, title и description.
        """
        query = """
        SELECT *
        FROM items
        WHERE items.user_is = user_id AND items.title = title AND items.description = description
        """
        input = [(enrty.item_id, entry.user_id, entry.title, entry.description) for entry in items]
	    async with self._pool.acquire() as cur_query:
            await connect.fetchmany(table_creation, input)

from typing import List, Optional, Tuple, TypeVar, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


async def create(
    session: AsyncSession,
    model: ModelType,
    **kwargs
) -> ModelType:
    """
    Создание объекта и возвращает его.

    Parameters:
    - session (AsyncSession): Асинхронная сессия для взаимодействия с БД.
    - model (ModelType): Тип модели SQLAlchemy.
    - **kwargs: Параметры для создания объекта.

    Returns:
        ModelType: Новый объект модели.
    """

    new_object = model(**kwargs)
    session.add(new_object)
    await session.commit()
    await session.refresh(new_object)
    return new_object


async def get_by_attributes(
    model: ModelType,
    attributes: dict,
    session: AsyncSession,
    get_multi: bool = False,
    amount: Optional[int] = None,
    order_by: Optional[str] = None
) -> Union[ModelType, List[ModelType]]:
    """
    Получение объекта/объектов по нескольким атрибутам.

    Parameters:
    - model (ModelType): Тип модели SQLAlchemy.
    - attributes (dict): Словарь атрибутов и их значений для фильтрации.
    - session (AsyncSession): Асинхронная сессия для взаимодействия с БД.
    - get_multi (bool): Флаг для получения нескольких объектов
                        (по умолчанию False).
    - amount (Optional[int]): Количество объектов для получения (опционально).
    - order_by (Optional[str]): Наименование поля для сортировки результатов
                                (опционально).

    Returns:
        Union[ModelType, List[ModelType]]: Объект или список объектов модели,
                                           удовлетворяющих условиям.
    """

    query = select(model).where(
        *[
            getattr(model, attr_name) == attr_value
            for attr_name, attr_value in attributes.items()
        ]
    )

    if order_by is not None:
        query = query.order_by(getattr(model, order_by).desc())

    if not get_multi:
        get_obj_in_db = await session.execute(query)
        return get_obj_in_db.scalars().first()

    if amount is not None:
        query = query.limit(amount)

    get_objs_in_db = await session.execute(query)
    return get_objs_in_db.scalars().all()


async def get_or_create(
    session: AsyncSession,
    model: ModelType,
    **kwargs
) -> Tuple[ModelType, bool]:
    """
    Получение или создание объекта.

    Parameters:
    - session (AsyncSession): Асинхронная сессия для взаимодействия с БД.
    - model (ModelType): Тип модели SQLAlchemy.
    - **kwargs: Параметры для фильтрации или создания объекта.

    Returns:
        Tuple[ModelType, bool]: Кортеж, содержащий объект модели и флаг,
                                указывающий на создание нового объекта.
    """

    instance = await session.execute(select(model).filter_by(**kwargs))
    instance = instance.scalars().one_or_none()
    flag = True

    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        flag = False
    return instance, flag


async def remove(
    db_obj: ModelType,
    session: AsyncSession,
) -> ModelType:
    """
    Удаление объекта.

    Parameters:
    - db_obj (ModelType): Объект модели для удаления.
    - session (AsyncSession): Асинхронная сессия для взаимодействия с БД.

    Returns:
        ModelType: Удаленный объект модели.
    """

    await session.delete(db_obj)
    await session.commit()
    return db_obj

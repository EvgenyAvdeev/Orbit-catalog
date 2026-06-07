import numpy as np
from models import (
    FilterGroup,
    FilterModel,
    LogicalOpEnum,
    QueryParamsModel,
    RepoBaseIdModel,
)
from models import FilterOpEnum as Op
from sqlalchemy import String, and_, cast, distinct, func, or_, select
from sqlalchemy.orm import Query, Session
from tables import Base

from .base import BaseRepo


class ReadRepo[TableType: Base, ReadModel: RepoBaseIdModel](
    BaseRepo[TableType, ReadModel]
):
    def __init__(self, table_class: type[TableType], read_model: type[ReadModel]):
        self.table_class = table_class
        self.read_model = read_model

    def to_read_model(self, record: TableType) -> ReadModel:
        if record is None:
            return None
        return self.read_model.model_validate(record)

    def to_read_model_list(self, records: list[TableType]) -> list[ReadModel]:
        return [self.to_read_model(record) for record in records]

    def get_record(self, id: int, session: Session) -> TableType:
        return session.get(self.table_class, id)

    def get(self, id: int, session: Session) -> ReadModel:
        record = self.get_record(id, session)
        return self.to_read_model(record)

    def build_query(
        self,
        session: Session,
        params: QueryParamsModel | None = None,
        query: Query | None = None,
        table_class: TableType | None = None,
    ) -> Query:
        if params is None:
            params = QueryParamsModel()

        if table_class is None:
            table_class = self.table_class

        if query is None:
            query = session.query(table_class)

        # filters = self.process_filters(params.filters, table_class)

        group_filters = self.process_filter_groups(params.filter_groups, table_class)

        all_filters = group_filters  # filters +

        if all_filters:
            query = query.filter(and_(*all_filters))

        if params.offset is not None:
            query = query.offset(params.offset)

        if params.limit is not None:
            query = query.limit(params.limit)

        return query

    # def process_filters(self, filters: list[FilterModel], table_class) -> list:
    #     result = []
    #     for filter_ in filters:
    #         if not hasattr(table_class, filter_.field):
    #             continue

    #         column = getattr(table_class, filter_.field)
    #         condition = self.build_condition(column, filter_)
    #         result.append(condition)

    #     return result

    def process_filter_groups(
        self, filter_groups: list[FilterGroup], table_class
    ) -> list:
        result = []
        for group in filter_groups:
            group_conditions = []

            for filter_ in group.filters:
                if not hasattr(table_class, filter_.field):
                    continue

                column = getattr(table_class, filter_.field)
                condition = self.build_condition(column, filter_)
                group_conditions.append(condition)

            if group_conditions:
                if (
                    group.log_op == LogicalOpEnum.AND
                    or group.log_op == LogicalOpEnum.NONE
                ):
                    result.append(and_(*group_conditions))
                else:
                    result.append(or_(*group_conditions))

        return result

    def build_condition(self, column, filter_: FilterModel):
        match filter_.op:
            case Op.lk:
                return cast(column, String).like(f"{filter_.value}")
            case Op.eq:
                return column == filter_.value
            case Op.ne:
                return column != filter_.value
            case Op.ge:
                return column >= filter_.value
            case Op.gt:
                return column > filter_.value
            case Op.le:
                return column <= filter_.value
            case Op.lt:
                return column < filter_.value

    def get_chunk_records(
        self, session: Session, params: QueryParamsModel | None = None
    ) -> list[TableType]:
        query = self.build_query(session, params)
        return query.all()

    def get_chunk(
        self, session: Session, params: QueryParamsModel | None = None
    ) -> list[ReadModel]:
        records = self.get_chunk_records(session, params)
        return self.to_read_model_list(records)

    def get_count(
        self, session: Session, params: QueryParamsModel | None = None
    ) -> int:
        query = self.build_query(session, params)
        return query.count()

    def get_nearest_orbit(self, session: Session, x: float, z: float) -> ReadModel:
        distance_expr = func.pow(self.table_class.x - x, 2) + func.pow(
            self.table_class.z - z, 2
        )
        query = session.query(self.table_class).order_by(distance_expr).limit(1)
        return self.to_read_model(query.first())

    def get_nearest_section(
        self, session: Session, x: float, z: float, plane: str
    ) -> ReadModel:
        distance_expr = func.pow(self.table_class.x - x, 2) + func.pow(
            self.table_class.z - z, 2
        )
        query = (
            session.query(self.table_class)
            .filter(self.table_class.plane == plane)
            .order_by(distance_expr)
        )
        res = query.first()
        return self.to_read_model(res)

    def get_next_orbit_by_id(
        self, session: Session, id: int, family_tag: str, lib_point: str
    ) -> ReadModel:
        filter = QueryParamsModel(
            filter_groups=[
                FilterGroup(
                    log_op=LogicalOpEnum.NONE,
                    filters=[
                        FilterModel(field="family_tag", op=Op.lk, value=family_tag),
                        FilterModel(field="lib_point", op=Op.lk, value=lib_point),
                    ],
                )
            ]
        )
        records = self.get_chunk_records(session, filter)
        orbit_ids = [record.orbit_id for record in records]
        max_id = max(orbit_ids)
        min_id = min(orbit_ids)
        if id == max_id:
            req_id = min_id
        else:
            req_id = id + 1
        query = (
            session.query(self.table_class)
            .filter(self.table_class.orbit_id == req_id)
            .limit(1)
        )
        return self.to_read_model(query.first())

    def get_prev_orbit_by_id(
        self, session: Session, id: int, family_tag: str, lib_point: str
    ) -> ReadModel:
        filter = QueryParamsModel(
            filter_groups=[
                FilterGroup(
                    log_op=LogicalOpEnum.NONE,
                    filters=[
                        FilterModel(field="family_tag", op=Op.lk, value=family_tag),
                        FilterModel(field="lib_point", op=Op.lk, value=lib_point),
                    ],
                )
            ]
        )
        records = self.get_chunk_records(session, filter)
        orbit_ids = [record.orbit_id for record in records]
        max_id = max(orbit_ids)
        min_id = min(orbit_ids)
        if id == min_id:
            req_id = max_id
        else:
            req_id = id - 1
        query = (
            session.query(self.table_class)
            .filter(self.table_class.orbit_id == req_id)
            .limit(1)
        )
        return self.to_read_model(query.first())

    def get_family_param(
        self,
        session: Session,
        lib_point: str,
        family_tag: str,
        param_name_x: str,
        param_name_y: str,
        param_name_z: str,
    ):
        from models import FamilyParamResponseModel

        filter = QueryParamsModel(
            filter_groups=[
                FilterGroup(
                    log_op=LogicalOpEnum.NONE,
                    filters=[
                        FilterModel(field="family_tag", op=Op.lk, value=family_tag),
                        FilterModel(field="lib_point", op=Op.lk, value=lib_point),
                    ],
                )
            ]
        )
        records = self.get_chunk_records(session, filter)
        result = []
        if param_name_x == "floke":
            for record in records:
                param_x = max(
                    record.floke_1_r,
                    record.floke_2_r,
                    record.floke_3_r,
                    record.floke_4_r,
                    record.floke_5_r,
                    record.floke_6_r,
                )
                param_y = getattr(record, param_name_y)
                param_z = getattr(record, param_name_z)
                result.append(
                    FamilyParamResponseModel(
                        orbit_id=record.orbit_id,
                        param_x=param_x,
                        param_y=param_y,
                        param_z=param_z,
                        x=record.x,
                        z=record.z,
                        cj=record.cj,
                    )
                )
        elif param_name_y == "floke":
            for record in records:
                param_y = max(
                    record.floke_1_r,
                    record.floke_2_r,
                    record.floke_3_r,
                    record.floke_4_r,
                    record.floke_5_r,
                    record.floke_6_r,
                )
                param_x = getattr(record, param_name_x)
                param_z = getattr(record, param_name_z)
                result.append(
                    FamilyParamResponseModel(
                        orbit_id=record.orbit_id,
                        param_x=param_x,
                        param_y=param_y,
                        param_z=param_z,
                        x=record.x,
                        z=record.z,
                        cj=record.cj,
                    )
                )
        elif param_name_z == "floke":
            for record in records:
                param_z = max(
                    record.floke_1_r,
                    record.floke_2_r,
                    record.floke_3_r,
                    record.floke_4_r,
                    record.floke_5_r,
                    record.floke_6_r,
                )
                param_x = getattr(record, param_name_x)
                param_y = getattr(record, param_name_y)
                result.append(
                    FamilyParamResponseModel(
                        orbit_id=record.orbit_id,
                        param_x=param_x,
                        param_y=param_y,
                        param_z=param_z,
                        x=record.x,
                        z=record.z,
                        cj=record.cj,
                    )
                )
        else:
            for record in records:
                param_x = getattr(record, param_name_x)
                param_y = getattr(record, param_name_y)
                param_z = getattr(record, param_name_z)
                result.append(
                    FamilyParamResponseModel(
                        orbit_id=record.orbit_id,
                        param_x=param_x,
                        param_y=param_y,
                        param_z=param_z,
                        x=record.x,
                        z=record.z,
                        cj=record.cj,
                    )
                )
        return result

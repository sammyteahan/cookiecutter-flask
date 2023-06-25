import datetime

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator
from flask_sqlalchemy import BaseQuery

from lib.util_datetime import tzware_datetime
from {{ cookiecutter.project_slug }}.extensions import db


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            raise ValueError('{!r} must be TZ-aware'.format(value))
        return value

    def __repr__(self):
        return 'AwareDateTime()'


class ResourceMixin(object):
    # Keep track when records are created and updated.
    created_on = db.Column(AwareDateTime(),
                           default=tzware_datetime)
    updated_on = db.Column(AwareDateTime(),
                           default=tzware_datetime,
                           onupdate=tzware_datetime)

    @classmethod
    def sort_by(cls, field, direction):
        """
        Validate the sort field and direction.

        :param field: Field name
        :type field: str
        :param direction: Direction
        :type direction: str
        :return: tuple
        """
        if field not in cls.__table__.columns:
            field = 'created_on'

        if direction not in ('asc', 'desc'):
            direction = 'asc'

        return field, direction

    @classmethod
    def get_bulk_action_ids(cls, scope, ids, omit_ids=[], query=''):
        """
        Determine which IDs are to be modified.

        :param scope: Affect all or only a subset of items
        :type scope: str
        :param ids: List of ids to be modified
        :type ids: list
        :param omit_ids: Remove 1 or more IDs from the list
        :type omit_ids: list
        :param query: Search query (if applicable)
        :type query: str
        :return: list
        """
        omit_ids = map(str, omit_ids)

        if scope == 'all_search_results':
            # Change the scope to go from selected ids to all search results.
            ids = cls.query.with_entities(cls.id).filter(cls.search(query))

            # SQLAlchemy returns back a list of tuples, we want a list of strs.
            ids = [str(item[0]) for item in ids]

        # Remove 1 or more items from the list, this could be useful in spots
        # where you may want to protect the current user from deleting themself
        # when bulk deleting user accounts.
        if omit_ids:
            ids = [id for id in ids if id not in omit_ids]

        return ids

    @classmethod
    def bulk_delete(cls, ids):
        """
        Delete 1 or more model instances.

        :param ids: List of ids to be deleted
        :type ids: list
        :return: Number of deleted instances
        """
        delete_count = cls.query.filter(cls.id.in_(ids)).delete(
            synchronize_session=False)
        db.session.commit()

        return delete_count

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)


class SoftDeleteQueryManager(BaseQuery):
    """
    Query manager that decorates a model with soft-delete functionality
    """

    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(SoftDeleteQueryManager, cls).__new__(cls)
        obj._with_deleted = kwargs.pop("_with_deleted", False)
        if len(args) > 0:
            super(SoftDeleteQueryManager, obj).__init__(*args, **kwargs)
            return (
                obj.filter_by(is_removed=False)
                if not obj._with_deleted
                else obj
            )
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        """
        Method used to retrieve models that have been soft-deleted
        """
        return self.__class__(
            self._only_full_mapper_zero("get"),
            session=db.session(),
            _with_deleted=True,
        )

    def _get(self, *args, **kwargs):
        """
        This calls the original query.get function from the base class
        """
        return super(SoftDeleteQueryManager, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Custom implementation of `get`. Query.get doesn't currently allow
        a filter clause pre-loaded which is why this is necessary.
        """
        obj = self.with_deleted()._get(*args, **kwargs)

        return (
            obj
            if obj is None or self._with_deleted or not obj.is_removed
            else None
        )

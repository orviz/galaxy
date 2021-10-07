from contextlib import contextmanager
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import (
    delete,
    select,
    UniqueConstraint,
)

import tool_shed.webapp.model.mapping as mapping


class BaseTest:
    @pytest.fixture
    def cls_(self, model):
        """
        Return class under test.
        Assumptions: if the class under test is Foo, then the class grouping
        the tests should be a subclass of BaseTest, named TestFoo.
        """
        prefix = len('Test')
        class_name = self.__class__.__name__[prefix:]
        return getattr(model, class_name)


class TestAPIKeys(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'api_keys'

    def test_columns(self, session, cls_, user):
        create_time, user_id, key = datetime.now(), user.id, get_unique_value()
        obj = cls_(user_id=user_id, key=key, create_time=create_time)

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.user_id == user_id
            assert stored_obj.key == key


class TestUser(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'galaxy_user'

    def test_columns(self, session, cls_):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        email = get_unique_value()
        username = get_unique_value()
        password = 'c'
        external = True
        new_repo_alert = True
        deleted = True
        purged = True

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.email = email
        obj.username = username
        obj.password = password
        obj.external = external
        obj.new_repo_alert = new_repo_alert
        obj.deleted = deleted
        obj.purged = purged

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.email == email
            assert stored_obj.username == username
            assert stored_obj.password == password
            assert stored_obj.external == external
            assert stored_obj.new_repo_alert == new_repo_alert
            assert stored_obj.deleted == deleted
            assert stored_obj.purged == purged


class TestPasswordResetToken(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'password_reset_token'

    def test_columns_and_relationships(self, session, cls_, user):
        token = get_unique_value()
        expiration_time = datetime.now()
        obj = cls_(user, token)
        obj.expiration_time = expiration_time

        where_clause = cls_.token == token

        with dbcleanup(session, obj, where_clause):
            stored_obj = get_stored_obj(session, cls_, where_clause=where_clause)
            # test columns
            assert stored_obj.token == token
            assert stored_obj.expiration_time == expiration_time
            assert stored_obj.user_id == user.id
            # test relationships
            assert stored_obj.user.id == user.id


class TestGroup(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'galaxy_group'

    def test_columns(self, session, cls_):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        name = get_unique_value()
        deleted = True

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.name = name
        obj.deleted = deleted

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.name == name
            assert stored_obj.deleted == deleted


class TestRole(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'role'

    def test_columns(self, session, cls_):
        name, description, type_, deleted = get_unique_value(), 'b', cls_.types.SYSTEM, True
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(name, description, type_, deleted)
        obj.create_time = create_time
        obj.update_time = update_time

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.name == name
            assert stored_obj.description == description
            assert stored_obj.type == type_
            assert stored_obj.deleted == deleted


class TestRepositoryRoleAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'repository_role_association'

    def test_columns(self, session, cls_, repository, role):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(repository, role)
        obj.create_time = create_time
        obj.update_time = update_time

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.repository_id == repository.id
            assert stored_obj.role_id == role.id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time


class TestUserGroupAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'user_group_association'

    def test_columns(self, session, cls_, user, group):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(user, group)
        obj.create_time = create_time
        obj.update_time = update_time

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.user_id == user.id
            assert stored_obj.group_id == group.id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time


class TestUserRoleAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'user_role_association'

    def test_columns(self, session, cls_, user, role):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj = cls_(user, role)
        obj.create_time = create_time
        obj.update_time = update_time

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.user_id == user.id
            assert stored_obj.role_id == role.id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time


class TestGroupRoleAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'group_role_association'

    def test_columns(self, session, cls_, group, role):
        obj = cls_(group, role)
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        obj.create_time = create_time
        obj.update_time = update_time

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.group_id == group.id
            assert stored_obj.role_id == role.id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time


class TestGalaxySession(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'galaxy_session'

    def test_columns(self, session, cls_, user, galaxy_session):

        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        remote_host = 'a'
        remote_addr = 'b'
        referer = 'c'
        session_key = get_unique_value()
        is_valid = True
        last_action = update_time + timedelta(hours=1)

        obj = cls_(user=user, prev_session_id=galaxy_session.id)

        obj.create_time = create_time
        obj.update_time = update_time
        obj.remote_host = remote_host
        obj.remote_addr = remote_addr
        obj.referer = referer
        obj.session_key = session_key
        obj.is_valid = is_valid
        obj.last_action = last_action

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.user_id == user.id
            assert stored_obj.remote_host == remote_host
            assert stored_obj.remote_addr == remote_addr
            assert stored_obj.referer == referer
            assert stored_obj.session_key == session_key
            assert stored_obj.is_valid == is_valid
            assert stored_obj.prev_session_id == galaxy_session.id
            assert stored_obj.last_action == last_action


class TestTag(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'tag'
        assert has_unique_constraint(cls_.table, ('name',))

    def test_columns(self, session, cls_):
        parent_tag = cls_()
        type_, name = 1, get_unique_value()
        obj = cls_(type=type_, name=name)
        obj.parent = parent_tag

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.type == type_
            assert stored_obj.parent_id == parent_tag.id
            assert stored_obj.name == name


class TestCategory(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'category'

    def test_columns(self, session, cls_):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        name, description, deleted = get_unique_value(), 'b', True

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.name = name
        obj.description = description
        obj.deleted = deleted

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.name == name
            assert stored_obj.description == description
            assert stored_obj.deleted == deleted


class TestRepository(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'repository'

    def test_columns(self, session, cls_, user):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        name = 'a'
        type = 'b'
        remote_repository_url = 'c'
        homepage_url = 'd'
        description = 'e'
        long_description = 'f'
        private = True
        deleted = True
        email_alerts = False
        times_downloaded = 1
        deprecated = True

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.name = name
        obj.type = type
        obj.remote_repository_url = remote_repository_url
        obj.homepage_url = homepage_url
        obj.description = description
        obj.long_description = long_description
        obj.user = user
        obj.private = private
        obj.deleted = deleted
        obj.email_alerts = email_alerts
        obj.times_downloaded = times_downloaded
        obj.deprecated = deprecated

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.name == name
            assert stored_obj.type == type
            assert stored_obj.remote_repository_url == remote_repository_url
            assert stored_obj.homepage_url == homepage_url
            assert stored_obj.description == description
            assert stored_obj.long_description == long_description
            assert stored_obj.user_id == user.id
            assert stored_obj.private == private
            assert stored_obj.deleted == deleted
            assert stored_obj.email_alerts == email_alerts
            assert stored_obj.times_downloaded == times_downloaded
            assert stored_obj.deprecated == deprecated
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.name == name
            assert stored_obj.description == description
            assert stored_obj.deleted == deleted


class TestRepositoryMetadata(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'repository_metadata'

    def test_columns(self, session, cls_, repository):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        changeset_revision = 'a'
        numeric_revision = 1
        metadata = 'b'
        tool_versions = 'c'
        malicious = True
        downloadable = False
        missing_test_components = True
        has_repository_dependencies = True
        includes_datatypes = True
        includes_tools = True
        includes_tool_dependencies = True
        includes_workflows = True

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.repository_id = repository.id
        obj.changeset_revision = changeset_revision
        obj.numeric_revision = numeric_revision
        obj.metadata = metadata
        obj.tool_versions = tool_versions
        obj.malicious = malicious
        obj.downloadable = downloadable
        obj.missing_test_components = missing_test_components
        obj.has_repository_dependencies = has_repository_dependencies
        obj.includes_datatypes = includes_datatypes
        obj.includes_tools = includes_tools
        obj.includes_tool_dependencies = includes_tool_dependencies
        obj.includes_workflows = includes_workflows

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.repository_id == repository.id
            assert stored_obj.changeset_revision == changeset_revision
            assert stored_obj.numeric_revision == numeric_revision
            assert stored_obj.metadata == metadata
            assert stored_obj.tool_versions == tool_versions
            assert stored_obj.malicious == malicious
            assert stored_obj.downloadable == downloadable
            assert stored_obj.missing_test_components == missing_test_components
            assert stored_obj.has_repository_dependencies == has_repository_dependencies
            assert stored_obj.includes_datatypes == includes_datatypes
            assert stored_obj.includes_tools == includes_tools
            assert stored_obj.includes_tool_dependencies == includes_tool_dependencies
            assert stored_obj.includes_workflows == includes_workflows


class TestRepositoryReview(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'repository_review'

    def test_columns(self, session, cls_, repository, user):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        changeset_revision = 'a'
        approved = 'b'
        rating = 1
        deleted = True

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.repository = repository
        obj.changeset_revision = changeset_revision
        obj.user = user
        obj.approved = approved
        obj.rating = rating
        obj.deleted = deleted

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.repository_id == repository.id
            assert stored_obj.changeset_revision == changeset_revision
            assert stored_obj.user_id == user.id
            assert stored_obj.approved == approved
            assert stored_obj.rating == rating
            assert stored_obj.deleted == deleted


class TestComponentReview(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'component_review'

    def test_columns(self, session, cls_, repository_review, component):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        comment = 'a'
        private = True
        approved = 'b'
        rating = 1
        deleted = True

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.repository_review = repository_review
        obj.component = component
        obj.comment = comment
        obj.private = private
        obj.approved = approved
        obj.rating = rating
        obj.deleted = deleted

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.repository_review_id == repository_review.id
            assert stored_obj.component_id == component.id
            assert stored_obj.comment == comment
            assert stored_obj.private == private
            assert stored_obj.approved == approved
            assert stored_obj.rating == rating
            assert stored_obj.deleted == deleted


class TestComponent(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'component'

    def test_columns(self, session, cls_):
        name, description = 'a', 'b'
        obj = cls_(name=name, description=description)

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.name == name
            assert stored_obj.description == description


class TestRepositoryRatingAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'repository_rating_association'

    def test_columns(self, session, cls_, repository, user):
        create_time = datetime.now()
        update_time = create_time + timedelta(hours=1)
        rating = 1
        comment = 'a'

        obj = cls_()
        obj.create_time = create_time
        obj.update_time = update_time
        obj.repository = repository
        obj.user = user
        obj.rating = rating
        obj.comment = comment

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.create_time == create_time
            assert stored_obj.update_time == update_time
            assert stored_obj.repository_id == repository.id
            assert stored_obj.user_id == user.id
            assert stored_obj.rating == rating
            assert stored_obj.comment == comment


class TestRepositoryCategoryAssociation(BaseTest):

    def test_table(self, cls_):
        assert cls_.table.name == 'repository_category_association'

    def test_columns(self, session, cls_, repository, category):
        obj = cls_(repository=repository, category=category)

        with dbcleanup(session, obj) as obj_id:
            stored_obj = get_stored_obj(session, cls_, obj_id)
            assert stored_obj.id == obj_id
            assert stored_obj.repository_id == repository.id
            assert stored_obj.category_id == category.id


# Misc. helper fixtures.

@pytest.fixture(scope='module')
def model():
    db_uri = 'sqlite:///:memory:'
    return mapping.init('/tmp', db_uri, create_tables=True)


@pytest.fixture
def session(model):
    Session = model.session
    yield Session()
    Session.remove()  # Ensures we get a new session for each test


@pytest.fixture
def category(model, session):
    instance = model.Category(name=get_unique_value())
    yield from dbcleanup_wrapper(session, instance)


@pytest.fixture
def component(model, session):
    instance = model.Component()
    yield from dbcleanup_wrapper(session, instance)


@pytest.fixture
def galaxy_session(model, session):
    instance = model.GalaxySession(session_key=get_unique_value())
    yield from dbcleanup_wrapper(session, instance)


@pytest.fixture
def group(model, session):
    instance = model.Group(name=get_unique_value())
    yield from dbcleanup_wrapper(session, instance)


@pytest.fixture
def repository(model, session):
    instance = model.Repository()
    yield from dbcleanup_wrapper(session, instance)


@pytest.fixture
def repository_review(model, session, user):
    instance = model.RepositoryReview()
    instance.user = user
    yield from dbcleanup_wrapper(session, instance)


@pytest.fixture
def role(model, session):
    instance = model.Role(name=get_unique_value())
    yield from dbcleanup_wrapper(session, instance)


@pytest.fixture
def user(model, session):
    instance = model.User(email=get_unique_value(), password='password')
    yield from dbcleanup_wrapper(session, instance)


# Test utilities

def dbcleanup_wrapper(session, obj, where_clause=None):
    with dbcleanup(session, obj, where_clause):
        yield obj


@contextmanager
def dbcleanup(session, obj, where_clause=None):
    """
    Use the session to store obj in database; delete from database on exit, bypassing the session.

    If obj does not have an id field, a SQLAlchemy WHERE clause should be provided to construct
    a custom select statement.
    """
    return_id = where_clause is None

    try:
        obj_id = persist(session, obj, return_id)
        yield obj_id
    finally:
        table = obj.table
        if where_clause is None:
            where_clause = _get_default_where_clause(type(obj), obj_id)
        stmt = delete(table).where(where_clause)
        session.execute(stmt)


def persist(session, obj, return_id=True):
    """
    Use the session to store obj in database, then remove obj from session,
    so that on a subsequent load from the database we get a clean instance.
    """
    session.add(obj)
    session.flush()
    obj_id = obj.id if return_id else None  # save this before obj is expunged
    session.expunge(obj)
    return obj_id


def get_stored_obj(session, cls, obj_id=None, where_clause=None, unique=False):
    # Either obj_id or where_clause must be provided, but not both
    assert bool(obj_id) ^ (where_clause is not None)
    if where_clause is None:
        where_clause = _get_default_where_clause(cls, obj_id)
    stmt = select(cls).where(where_clause)
    result = session.execute(stmt)
    # unique() is required if result contains joint eager loads against collections
    # https://gerrit.sqlalchemy.org/c/sqlalchemy/sqlalchemy/+/2253
    if unique:
        result = result.unique()
    return result.scalar_one()


def _get_default_where_clause(cls, obj_id):
    where_clause = cls.table.c.id == obj_id
    return where_clause


def has_unique_constraint(table, fields):
    for constraint in table.constraints:
        if isinstance(constraint, UniqueConstraint):
            col_names = {c.name for c in constraint.columns}
            if set(fields) == col_names:
                return True


def get_unique_value():
    """Generate unique values to accommodate unique constraints."""
    return uuid4().hex

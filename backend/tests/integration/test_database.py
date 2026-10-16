from sqlalchemy import text

from app.db.models import User
from app.db.session import create_session_factory, create_sqlite_engine, session_scope


def test_sqlite_connection_enables_required_pragmas(tmp_path):
    engine = create_sqlite_engine(f"sqlite:///{(tmp_path / 'pragmas.db').as_posix()}")
    with engine.connect() as connection:
        assert connection.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
        assert connection.execute(text("PRAGMA journal_mode")).scalar_one().lower() == "wal"
        assert connection.execute(text("PRAGMA busy_timeout")).scalar_one() == 5000


def test_session_scope_rolls_back_failed_transaction(tmp_path):
    engine = create_sqlite_engine(f"sqlite:///{(tmp_path / 'rollback.db').as_posix()}")
    User.metadata.create_all(engine)
    factory = create_session_factory(engine)

    try:
        with session_scope(factory) as session:
            session.add(User.new("Carla", "carla@example.com", "hash"))
            raise RuntimeError("force rollback")
    except RuntimeError:
        pass

    with session_scope(factory) as session:
        assert session.query(User).count() == 0


def test_file_database_persists_after_engine_recreation(tmp_path):
    url = f"sqlite:///{(tmp_path / 'persistent.db').as_posix()}"
    engine = create_sqlite_engine(url)
    User.metadata.create_all(engine)
    with session_scope(create_session_factory(engine)) as session:
        session.add(User.new("Carla", "carla@example.com", "hash"))
    engine.dispose()

    recreated = create_sqlite_engine(url)
    with session_scope(create_session_factory(recreated)) as session:
        assert session.query(User).filter_by(email="carla@example.com").one().display_name == "Carla"

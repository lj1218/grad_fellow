# -*- coding:utf-8 -*-
"""Test cmd."""
from grad_fellow.models import Administrator


def test_init_db_command(runner, monkeypatch):
    """Test cmd 'init-db'."""
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('grad_fellow.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_set_admin_password_command(app, runner, monkeypatch):
    """Test cmd 'set-admin-password'."""
    password = '123456'
    result = runner.invoke(args=['set-admin-password'], input=password + '\n')
    assert 'set password to {} success'.format(password) in result.output

    # delete 'admin' from db
    from grad_fellow.db import db
    with app.app_context():
        administrator = Administrator.query.filter_by(name='admin').first()
        db.session.delete(administrator)
        db.session.commit()
    # if 'admin' does not exist, it will be created when set password
    result = runner.invoke(args=['set-admin-password'], input=password + '\n')
    assert 'set password to {} success'.format(password) in result.output

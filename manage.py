import os
import unittest
from flask_script import Manager

from app import app

manager = Manager(app)

@manager.command
def test(pattern='test*.py', test_package=''):
    """Runs the unit tests without test coverage."""
    tests_dir = 'app/tests/' + test_package
    tests = unittest.TestLoader().discover(tests_dir, pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def list_routes():
    """Lists application routes"""
    import urllib
    from flask import url_for
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        #
        methods = ','.join(rule.methods)
        line = ("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)

if __name__ == '__main__':
    manager.run()

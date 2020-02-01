#!/bin/bash -xe
coverage run --concurrency=multiprocessing manage.py test
coverage combine
coverage html
coverage report

#!/bin/bash -xe
black pyazo
scripts/coverage.sh
pylint pyazo
prospector
bandit -r pyazo

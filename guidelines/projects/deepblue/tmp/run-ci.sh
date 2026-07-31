#!/usr/bin/env bash
export JAVA_HOME="$(/usr/libexec/java_home -v 1.8)"
cd "/Users/gkostin/GitHub/mlibrary/deepblue"
exec bundle exec rake ci


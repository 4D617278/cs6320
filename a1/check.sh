#!/usr/bin/env bash

# Get total word counts
find . -name "*.txt" -exec wc -c '{}' \;

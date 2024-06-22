#!/bin/bash

# Navigate to the Go source directory
cd src

# Build the Go shared library including both Go files
go build -o ../class_scheduler.so -buildmode=c-shared scheduler.go 

# Move back to the root directory
cd ..


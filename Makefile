# The binary to build (just the basename).
MODULE := blueprint

# Where to push the docker image.
REGISTRY ?= docker.pkg.github.com/martinheinz/python-project-blueprint

IMAGE := $(REGISTRY)/$(MODULE)

# This version-strategy uses git tags to set the version string
TAG := $(shell git describe --tags --always --dirty)

BLUE='\033[0;34m'
NC='\033[0m' # No Color

run-mc-server:
	@python3 -m $(MODULE)

run-qt-client:
	@python3 -m $(MODULE).qt_client

run-echo-client:
	@python3 -m $(MODULE).echo_client

run-water-pump-test:
	@python3 -m $(MODULE).test.test_water_pump

grpc-gen:
	@python3 -m grpc_tools.protoc \
			-I $(MODULE)/proto \
			--python_out=./$(MODULE)/generated \
			--grpc_python_out=./$(MODULE)/generated \
			./$(MODULE)/proto/*.proto
	@sed -i -E 's/^\(import.*_pb2\)/from . \1/' ./$(MODULE)/generated/*.py


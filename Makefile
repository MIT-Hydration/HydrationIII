# The binary to build (just the basename).
MODULE := blueprint

run-mc-server:
	@python3 -m $(MODULE)

run-cs-server:
	@python3 -m $(MODULE).core_sensors_server

run-qt-client:
	@python3 -m $(MODULE).qt_client

run-echo-client:
	@python3 -m $(MODULE).echo_client

run-cs-client:
	@python3 -m $(MODULE).core_sensors_client

run-water-pump-test:
	@python3 -m $(MODULE).test.test_water_pump

run-drill-high-v-test:
	@python3 -m $(MODULE).test.drill_high_vtest1

run-drill-origin:
	@python3 -m $(MODULE).test.drill_back_to_origin

hydration-servo:
	@python3 blueprint/setup-HydrationServo.py build_ext --inplace

grpc-gen:
	@python3 -m grpc_tools.protoc \
			-I $(MODULE)/proto \
			--python_out=./$(MODULE)/generated \
			--grpc_python_out=./$(MODULE)/generated \
			./$(MODULE)/proto/*.proto
	@sed -i.bk 's/^\(import.*_pb2\)/from . \1/' ./$(MODULE)/generated/*.py 


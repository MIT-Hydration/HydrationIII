python3 -m grpc_tools.protoc --proto_path ./blueprint/proto \
        --python_out=./blueprint/generated \
        --grpc_python_out=./blueprint/generated \
        ./blueprint/proto/*.proto

sed -i -E 's/^import.*_pb2/from . \0/' ./blueprint/generated/*.py
clean:
	rm -rf HelloWorld TestRun
	rm -rf *.o
	rm -rf *.d
	rm -rf build
	rm -rf *.so

hello:
	g++ -I"/home/hydration/ClearPath/inc/inc-pub" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"HelloWorld.d" -MT"HelloWorld.o" -o "HelloWorld.o" "HelloWorld.cpp"
	g++ -pthread -o "HelloWorld" ./HelloWorld.o   -lsFoundation20

test-run:
	g++ -I"/home/hydration/ClearPath/inc/inc-pub" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"TestRun.d" -MT"TestRun.o" -o "TestRun.o" "TestRun.cpp"
	g++ -pthread -o "TestRun" ./TestRun.o   -lsFoundation20

pants:
	python3 setup.py build_ext --inplace

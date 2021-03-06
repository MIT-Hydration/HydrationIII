clean:
	rm -rf HelloWorld
	rm -rf *.o
	rm -rf *.d

hello:
	g++ -I"/home/hydration/ClearPath/inc/inc-pub" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"HelloWorld.d" -MT"HelloWorld.o" -o "HelloWorld.o" "HelloWorld.cpp"

test-run:
	g++ -I"/home/hydration/ClearPath/inc/inc-pub" -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"TestRun.d" -MT"TestRun.o" -o "TestRun.o" "TestRun.cpp"

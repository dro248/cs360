#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

// C++ includes
#include <iostream>
#include <vector>
#include <thread>
#include <mutex>

#include "task.h"

using namespace std;

void write_(Task* task) {
	task->write();
}

void read_(Task* task) {
	task->read();
}

int main(int argc, char **argv) {
	mutex m;
	Task* task = new Task(&m);
	
	thread a;
	thread b;
	a = thread(write_, task);
	b = thread(read_, task);
	
	a.join();
	b.join();
}


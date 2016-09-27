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

using namespace std;

int globyl = 0;

void storeInt(int a, mutex* m) {
	m->lock();
	cout << "Storing " << a << endl;
	globyl = a;
	m->unlock();
}

void readInt() {
	cout << "Reading " << globyl << endl;
}
	

int main(int argc, char **argv) {
	mutex m;
	
	thread a;
	thread b;
	a = thread(storeInt, rand()%100, &m);
	b = thread(readInt);
	
	a.join();
	b.join();
}


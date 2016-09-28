#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

void make_item(mutex* m,int* led) {
	while (1) {
		//do task
		m->lock();
		*items++;
		m->unlock();
	}
}

int main(int argc, char** argv) {
	int i = 0;
	int *led = &i;

	thread a;
	thread b;
	mutex m;

	a = thread(make_item,&m,&led);
	b = thread(make_item,&m,&led);

	a.join();
	b.join();
}


#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

void make_item(semaphore* sem,int* led) {
	while (1) {
		//do task
		semaphore->wait();
		*items++;
		semaphore->signal();
	}
}

int main(int argc, char** argv) {
	int i = 0;
	int *led = &i;

	thread a;
	thread b;
	semaphore sem;

	a = thread(make_item,&sem,&led);
	b = thread(make_item,&sem,&led);

	a.join();
	b.join();
}


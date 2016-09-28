#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

class Task {
private:
	mutex* mutex_;
	int* num_;
public:
	Task(mutex* m) {
		mutex_ = m;
		int temp = 0;
		num_ = &temp;
	}
	
	void write() {
		srand(time(NULL));
		int i = rand()%100;
		cout << "Storing " << i << endl;
		num_ = &i;
	}
	
	void read() {
		cout << "Reading " << *num_ << endl;
	}
};


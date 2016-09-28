#include <iostream>
#include <vector>
#include <mutex>
#include <condition_variable>
#include <thread>

#include <unistd.h>

using namespace std;

const int ORDER_MAX = 15;

typedef struct factory_params {
	vector<int>* orders;
	condition_variable *order_ready;
	condition_variable *order_waiting;
	mutex *m;
	int *num_orders;
	int *orders_processed;
} factory_params;

void head_robot_run(factory_params params) {
	while (*params.orders_processed<ORDER_MAX) {
		//assume that the list of orders is not thread safe
		unique_lock<mutex> u_lock(*params.m);
		while (params.orders->size() == 0) {
			params.order_waiting->wait(u_lock);
		}
		// preparing the order
		cout << "Order: " << params.orders->at(0) << " ready." << endl;
		params.orders->erase(params.orders->begin());
		(*params.orders_processed)++;
		// means the robots have made the order
		// and it is ready for delivery
		params.order_ready->notify_one();
	}
	// handle thread cancellation
}

void drone_run(factory_params params) {
	while (*params.num_orders<ORDER_MAX) {
		// placing an order
		int an_order = rand() % 100;
	
		params.m->lock();
		if (*params.num_orders >= 15) {
			params.m->unlock();
			break;
		}
		cout << "Adding order: " << an_order << endl;
		params.orders->push_back(an_order);
		params.order_waiting->notify_one();
		// increment the amount of orders placed
		(*params.num_orders)++;
		params.m->unlock();
	}
	// handle thread cancellation
}

int main(int argc, char** argv) {
	srand(time(NULL));
	vector<int> orders;
	// order ready means an order is ready for
	// delivery
	condition_variable order_ready;
	// order waiting means the drones placed an order
	condition_variable order_waiting;
	mutex m;

	thread head_robot;
	vector<thread> drones;
	int num_drones = 5;
	int zero = 0;
	int zero_ = 0;

	factory_params prms = {
		.orders = &orders,
		.order_ready = &order_ready,
		.order_waiting = &order_waiting,
		.m = &m,
		.num_orders = &zero,
		.orders_processed = &zero_
	};
	
	head_robot = thread(head_robot_run,prms);
	for (int i = 0; i < num_drones; ++i) {
		//make drones
		drones.push_back(thread(drone_run,prms));
	}

	// wait for the threads to all come back
	head_robot.join();
	for (int i = 0; i < drones.size(); ++i) {
		drones[i].join();
	}
	cout << *prms.num_orders<< endl;
	cout << *prms.orders_processed << endl;
	return 0;
}


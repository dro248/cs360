
//PSEUDO code
def make_item(basket,sem,basket_empty) {
	while (1) {
		item = make_item();
		sem->wait();
		basket.add(item);
		basket_empty.nofity_all();
		sem->signal();
	}
	//thread cancellation
}

def modify_item(basket,sem,basket_empty) {
	while (1) {
		sem->wait();
		item = basket.remove_one();
		basket_full.notify();
		sem->signal();
		item.put_on_conveyour_belt();
	}
}

def main() {
	list<robot> red;
	list<robot> blue;
	Basket basket;
	conditionvariable basket_full;
	conditionvariable basket_empty;
	semaphore sem;
	
	for all red robots {
		redbot = thread(make_item,basket,sem);
	}
	for all blue robots {
		bluebot = thread(modify_item,basket,sem);
	}
}


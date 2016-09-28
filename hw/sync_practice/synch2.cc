
//PSEUDO code
def make_item(basket,m,basket_empty) {
	while (1) {
		item = make_item();
		m.lock();
		while (basket.isFull)
			//auto unlocks when it goes to sleep
			basket_full.wait(m);
		basket.add(item);
		basket_empty.nofity_all();
		m.unlock(m);
	}
	//thread cancellation
}

def modify_item(basket,m,basket_empty) {
	while (1) {
		m.lock();
		// isEmpty is likely not thread safe so we lock it when we check
		while (basket.isEmpty())
			//auto unlocks the basket
			basket_empty.wait(m);
		item = basket.remove_one();
		basket_full.notify();
		m.unlock();
		item.put_on_conveyour_belt();
	}
}

def main() {
	list<robot> red;
	list<robot> blue;
	Basket basket;
	conditionvariable basket_full;
	conditionvariable basket_empty;
	mutext m;
	
	for all red robots {
		redbot = thread(make_item,basket,m);
	}
	for all blue robots {
		bluebot = thread(modify_item,basket,m);
	}
}


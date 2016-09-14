#include <iostream>
#include <string>

using namespace std;

class Message {
private:
	string command;
	string name;
	int length;
	string value;

public:
	Message();
	~Message();
	bool needed();

	/********************\
	 Getters and setters
	\********************/

	string getCommand();
	string getName();
	int getLength();
	string getValue();
	void setCommand(string command);
	void setName(string name);
	void setLength(int length);
	void setValue(string value);
};
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class Message {
private:
	string command;
	string name;
	int length;
	string value;
	vector<string> cmd_fields;

public:
	Message();
	~Message();
	bool needed();
	bool hasMessage();

	/********************\
	 Getters and setters
	\********************/

	string getCommand();
	string getName();
	int getLength();
	string getValue();
	vector<string> getCmdFields();
	void setCommand(string);
	void setName(string);
	void setLength(int);
	void setValue(string);
	void setCmdFields(vector<string>);
};
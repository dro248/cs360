#include "message.h"

Message::Message() {
	command = "";
	name = "";
	length = 0;
	value = "";
}

Message::~Message() {

}

bool Message::needed() {
	return false;
}

bool Message::hasMessage() {
	return command=="put";
}

/********************\
 Getters and setters
\********************/

string Message::getCommand() {
	return command;
}

string Message::getName() {
	return name;
}

int Message::getLength() {
	return length;
}

string Message::getValue() {
	return value;
}

vector<string> Message::getCmdFields() {
	return cmd_fields;
}

void Message::setCommand(string command) {
	this->command = command;
}

void Message::setName(string name) {
	this->name = name;
}

void Message::setLength(int length) {
	this->length = length;
}

void Message::setValue(string value) {
	this->value = value;
}

void Message::setCmdFields(vector<string> cf) {
	this->cmd_fields = cf;
}
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
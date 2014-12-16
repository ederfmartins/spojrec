Overview
========
This is a simple project to provide recommendations (of good problems) to spoj users.
Currenty, this project is only meant for educational purposes.

Requirements
============

* Python 2.7
	* Python modules
		* scrapy
		* pymongo
		* WebOb
		* Paste
		* webapp2
* mongodb

Install
=======

The quick way::

	clone the project from github (git clone https://github.com/ederfmartins/spojrec.git).
	use pip to install the python modules needed.
	edit constants.py and set variable values acording your environment.
	run start.sh to crawl necessary data.
	run python wscgi.py to start the web service.




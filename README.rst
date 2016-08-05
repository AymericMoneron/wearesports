WeAreSports Command-line interface
==================================

This is a command-line script (``wearesports``) for managing activity booking on `wearesports.fri`_, a sports complex in Lyon, France.

. _wearesports.fr: http://www.wearesports.fr


Command-line script
===================

Installing this package gets you a shell command, ``wearesports``, that you can use to interact with `wearesports.fr`_.

You'll need to provide your WeAreSports credentials. You can do this with the ``--username`` and ``--password`` params, but it's easier to just set them as environment variables:

	export WAS_USERNAME=<username>
	export WAS_PASSWORD=<password>

Usage
=====

List available courts for badminton :

	wearesports badminton schedule $(date +%Y-%m-%d)


Activities to do
================

* Badminton ``badminton``
* Squash ``squash``
* Padel ``padel``
* Foot XL ``foot``
* Foot 5 ``foot_5``

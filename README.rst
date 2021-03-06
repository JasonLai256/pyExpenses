==========
pyExpenses
==========
pyExpenses is a python package for simply personally financial management.

The purpose of pyExpenses is to provide a easy way - simple api invoke - to
manage daily trivial expenses, and make it easy to analyze and statistic
user records.


Features
--------
* provide a set of api that easy to use to control all the things about
  manage expenses;

* surport a flexible and scalable mechanism for expenses storage, could
  choose different storage backend from configuration(now has the Pickle
  implementation, suppose will add the SQLite implementation in the future);

* record parser that analyze user data has three types, including 'filter',
  'analyzing' and 'statistic';

* record parser is base on composition pattern, can flexibly compose parsers;

* surport project concept that let the application can automatic to do many
  useful thing for the user;

* more project types will be provide;

* ...


Frame of Package
----------------

::

                    +-------------------+
                    | (Storage Backend) |
                    |    RecManipImpl   |
                    |                   |
                    +------+------------+         +--------------+
                           |                      |              |
                           |                      |  ErrorHandle |
                           V                      |              |
                      +-----------+               +--------------+
                      |           |
      +-------------->|  RecManip |
      |               |           |
      |               +----+------+
      |                    |                   (manage)
      |                    |       +-------------+-----------------+
      |                    |       |             |                 |
      |                    V       |             |                 |
      |              +-------------+-+           V                 V
 +----+--------+     |               |      +-----------+     +----------+
 |             |     |  (Scheduler)  |      |           |     |          |
 | ConfigManip +---->|    Expense    |      | RecParser |     | Projects |
 |             |     |               |      |           |     |          |
 +-----+-------+     |               |      +----+------+     +-----+----+
       |             +--------+------+           |                  |
       |                      |       +----------+                  |
       |                      |       |        +--------------------+
       |                      |       |        |
       |                      V       V        V
       |                   +---------------------+
       +------------------>|                     |
                           |        USER         |
                           | (developer use api) |
                           |                     |
                           +---------------------+


Installation
------------
Installation is simple. You can install it by running::

    $ pip install pyExpenses

Or to get the latest development version from git::

    $ git clone git://github.com/JasonLai256/pyExpenses.git


Support
-------
You can log issues on the Github issue tracker for this project.
And welcome you can collaborate with the author to maintain this project.

- [Initialization](#initialization)
- [pytest django 0](#pytest-django-0)
    + [Install the Plugin: pytest django](#install-the-plugin-pytest-django)
    + [Create a Django App](#create-a-django-app)
    + [Start a Django Shell](#start-a-django-shell)
    + [Run](#run)
    + [Observe](#observe)
- [pytest django 1](#pytest-django-1)
    + [Run](#run-1)
    + [Observe](#observe-1)
- [Experiments: Fixtures Modify The Database](#experiments-fixtures-modify-the-database)
      - [Run](#run-2)
      - [Observe](#observe-2)
- [Experiments: Oxymoron](#experiments-oxymoron)
      - [Run](#run-3)
      - [Observe](#observe-3)
- [Experiments: Oxy2](#experiments-oxy2)
      - [Run](#run-4)
      - [Observe](#observe-4)
- [Experiments: django_db_setup interferance](#experiments-django_db_setup-interferance)
      - [Run](#run-5)
      - [Observe](#observe-5)
- [Experiments: watch the database](#experiments-watch-the-database)
      - [Run](#run-6)
      - [Observe](#observe-6)
- [factoryboy](#factoryboy)
      - [Basic Factoryboy Usage](#basic-factoryboy-usage)
      - [Sequences](#sequences)
      - [Post Generation](#post-generation)
      - [build vs create](#build-vs-create)
      - [Lazy Functions](#lazy-functions)
      - [Lazy Attributes:](#lazy-attributes)
      - [Non KWarg args:](#non-kwarg-args)
      - [Parameters and Traits](#parameters-and-traits)
      - [build vs. create](#build-vs-create)
- [Fixture with Module Scope](#fixture-with-module-scope)
    + [Run commands](#run-commands)
    + [Observe output](#observe-output)
      - [RIDDLE:](#riddle)
      - [EXPLANATION:](#explanation)
- [Module Caching](#module-caching)
  * [Run these commands](#run-these-commands)
  * [Observe output](#observe-output-1)
- [Autouse](#autouse)
  * [Run these commands](#run-these-commands-1)
  * [Observe output and code](#observe-output-and-code)
- [scope sharing fixtures across classes modules packages or session](#scope-sharing-fixtures-across-classes-modules-packages-or-session)
  * [Run](#run-7)
  * [Observe](#observe-7)
- [Scope 0](#scope-0)
  * [Run these commands](#run-these-commands-2)
  * [Examine code, Observe output and code](#examine-code-observe-output-and-code)
- [Fixture Errors](#fixture-errors)
  * [run](#run)
  * [observe](#observe)
- [Fixture Availability](#fixture-availability)
  * [Run](#run-8)
  * [Observe](#observe-8)
  * [Run](#run-9)
  * [Observe](#observe-9)
- [conftest.py: sharing fixtures across multiple files](#conftestpy-sharing-fixtures-across-multiple-files)
  * [Run](#run-10)
  * [Observe](#observe-10)
  * [Run](#run-11)
  * [Observe](#observe-11)
- [higher-scoped-fixtures-are-executed-first](#higher-scoped-fixtures-are-executed-first)
  * [Run](#run-12)
  * [Observe](#observe-12)
- [running-multiple-assert-statements-safely](#running-multiple-assert-statements-safely)
  * [Run](#run-13)
  * [Observe](#observe-13)
- [fixtures-can-introspect-the-requesting-test-context](#fixtures-can-introspect-the-requesting-test-context)
  * [Run](#run-14)
  * [Observe](#observe-14)
- [Match Error Messages](#match-error-messages)
# Initialization

```
python3 -m venv testenv
source testenv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

```
# pytest django 0
this is the code along for the
[quick start](https://pytest-django.readthedocs.io/en/latest/#quick-start)
and the
[configuring django](https://pytest-django.readthedocs.io/en/latest/configuring_django.html)
sections of the pytest-django docs.

### Install the Plugin: pytest django
```
source testenv/bin/activate
python -m pip upgrade pip
python -m pip install pytest-django
```

### Create a Django App
```
source testenv/bin/activate
python -m pip install django
python -m pip install ipython
django-admin startproject mysite
python mysite/manage.py migrate
```

### Start a Django Shell
```
source testenv/bin/activate
python mysite/manage.py shell
```

### Run
```
PYTHONPATH=/Users/stephen.french/pytest-examples/mysite pytest django_plugin --ds=mysite.settings
```

### Observe

test0 requests the settings fixture. If you examine the output from the test, and the
settings for the discovered Django Project, you can see that the settings fixture is
populated with the values from the settings file of the discovered Django Project.

test1 sets the settings.DEBUG to be True

test2 asserts settings.DEBUG is True, which evalutes to false and fails the test.

# pytest django 1
This is the code along for the
[Database Access](https://pytest-django.readthedocs.io/en/latest/database.html)
section of the pytest django documentation.

Do a django thing in the shell (after completing pytest django 0)
This is just to show that a model exists, as does the table in the database, and that it all works.
Note that you don't actually need the database to exist in order to test the model. 
```
python mysite/manage.py shell
from django.contrib.auth.models import User
user=User.objects.create_user('foo', password='bar')
user.is_superuser=True
user.is_staff=True
user.save()
assert len(User.objects.all()) == 1
```

### Run 
```
PYTHONPATH=/Users/stephen.french/pytest-examples/mysite pytest django_db --ds=mysite.settings
```

### Observe
The test successfully executes code that interacts with a database. 
Both tests add 1 user to the database and then assert that there is one user.
Both tests are successful. 
This shows that the database is unaffected by the execution of the test.

# Experiments: Fixtures Modify The Database
Can I add an entry to the test database with one fixture, so that I can access it with another fixture?
The [relevant section of the docs](https://pytest-django.readthedocs.io/en/latest/helpers.html#pytest-mark-django-db-request-database-access)
The idea is that each test gets a transaction that is rolled back at the end of the test. 

#### Run
```
PYTHONPATH=/Users/stephen.french/pytest-examples/mysite pytest experiments/fixtures_modify_the_database/test0.py --ds=mysite.settings
```

#### Observe
Both tests add an entry to the database via a fixture.
Both tests successfully retrieve the entry they added.
Both tests show they cannot retrieve the entry added by the other test. 

# Experiments: Oxymoron
A Module-scoped fixture that modifies the database is an oxymoron.


#### Run
```
PYTHONPATH=/Users/stephen.french/pytest-examples/mysite pytest experiments/oxymoron/test0.py --ds=mysite.settings
```

#### Observe
The test requests a fixture.
The fixture is scoped to the module.
The fixture definition calls for a new database object. 
The test errors on setup.

# Experiments: Oxy2
When an autouse fixture is defined in a modulet that contains a class with tests,
the tests in the class request the autouse fixture as scoped in the function definition,
rather than the class as a whole automatically requesting the autofixture as scoped to the class.
So this is not an oxymoron.


#### Run
```
PYTHONPATH=/Users/stephen.french/pytest-examples/mysite pytest experiments/oxy2/test0.py --ds=mysite.settings
```

#### Observe
No errors, everythin passes, because the tests in the class consume the fixture as being scoped to the function.

# Experiments: django_db_setup interferance
You can scope a fixture to the module, and then add to the database.
I know, that is supposed to be an oxymoron.
But when you use this special fixture called django_db_setup,
then you CAN do this stuff. 

But be careful, you are modifying the test database permanently.


#### Run
```
PYTHONPATH=/Users/stephen.french/pytest-examples/mysite pytest experiments/django_db_setup/test0.py --ds=mysite.settings
```

#### Observe
The test requests a fixture.
The fixture is scoped to the module.
The fixture definition calls for a new database object. 
The test errors on setup.

# Experiments: watch the database

#### Run
```
python manage.py migrate
PYTHONPATH=/Users/stephen.french/pytest-examples/mysite pytest experiments/watch/test0.py --ds=mysite.settings --reuse-db
python manage.py dbshell
.tables
select * from polls_question;

python manage.py shell
# modify the database
```

#### Observe

# factoryboy
This is the code-along for the
[basic usage section](https://factoryboy.readthedocs.io/en/stable/introduction.html#basic-usage)
of the factoryboy plugin.


#### Basic Factoryboy Usage
Venv, for reference
```
source testenv/bin/activate
```

Start django shell against clean database
```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell
```

Background:
Django manages the pk and assigns at save.
pks start at 1
```
from django.contrib.auth.models import User 
ben = User(username='ben')
assert ben.id == None
ben.save()
assert ben.id == 1

tom = User(username='max')
assert tom.id == None
tom.save()
tom.id == 2
```

Use a Factory to instantiate a User.
The factory offers defaults for all fields.
```
from factoryboy_example.example_factories import ExampleUserFactory
default = ExampleUserFactory()
# Check Default fields
default.username == 'default'
default.password == 'default'
default.is_superuser == True
default.is_staff == True
default.email == 'default'
```

The User has a custom email and username. 
```
from factoryboy_example.example_factories import ExampleUserFactory
stephen = ExampleUserFactory(username='stephen', email='stephen@stephen.com')
# Check Default fields
stephen.email == 'default'
stephen.password == 'default'
stephen.is_superuser == True
stephen.is_staff == True
# Check Custom fields
stephen.username == 'stephen' 
stephen.email == 'stephen@stephen.com'
```

Confirm that ids exist, and rows were saved to the database.
pks start at 1.
```
ben.id == 1
tom.id == 2
default.id == 3
stephen.id == 4
exit()
python mysite/manage.py shell
from django.contrib.auth.models import User
len(User.objects.all()) == 4
```

#### Sequences
[Sequences](https://factoryboy.readthedocs.io/en/stable/introduction.html#sequences)

What if you want to make a bunch of default users in a row?
```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

from factoryboy_example.example_factories import ExampleUserFactory
default = ExampleUserFactory()
default1 = ExampleUserFactory()
default2 = ExampleUserFactory()
```

It errors, because they all have the same username. 
You can write a factory that generates a new username each time it is called.
```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

from factoryboy_example.example_factories import ExampleUserFactory_sequence
default_1 = ExampleUserFactory_sequence()
default_2 = ExampleUserFactory_sequence()
default_3 = ExampleUserFactory_sequence()

assert default_1.id == 1
assert default_1.username == 'default_0'
assert default_2.id == 2
assert default_2.username == 'default_1'
assert default_3.id == 3
assert default_3.username == 'default_2'
```

Note that the factory sequence started at 0. Would have been nice if it had started at 1.
Easy enough to fix with a +1.

Let us demonstrate that there is only one sequence. 
It is shared between attributes.
Let us use a sequence to start the pk at 0, along with the username, so that pk and username use the same integer.
```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

from factoryboy_example.example_factories import ExampleUserFactory_one_sequence
default_0 = ExampleUserFactory_one_sequence()
default_1 = ExampleUserFactory_one_sequence()
default_2 = ExampleUserFactory_one_sequence()

assert default_0.id == 0
assert default_0.username == 'default_0'
assert default_1.id == 1
assert default_1.username == 'default_1'
assert default_2.id == 2
assert default_2.username == 'default_2'
```

We saw above that (0, 1,2,3,4 ...) is shared between attributes. Moreover, the docs promise that
the sequence belongs to the mother class. If any child class requests for an integer from the sequence 
to incorporate into a field, that sequence increments to the next integer, and the mother class will get a
different int the next time it makes a request to the sequence.
[Inheritance With Regards to the Sequence](https://factoryboy.readthedocs.io/en/stable/reference.html#inheritance)
```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

# reference the sequence from the child class
from factoryboy_example.example_factories import ExampleUserFactory_one_sequence
default_0 = ExampleUserFactory_one_sequence()
assert default_0.id == 0 # The sequence starts at 0
assert default_0.username == 'default_0' # The sequence starts at 0

# reference the sequence from the mother class
from factoryboy_example.example_factories import ExampleUserFactory_sequence
default_1 = ExampleUserFactory_sequence()
assert default_1.id == 1 # The pk got autoincremented by sql
assert default_1.username == 'default_1' # The sequence has gotten to 1

# and lets look at the squence from the child class
default_2 = ExampleUserFactory_one_sequence()
assert default_2.id == 2 # The sequence is at 2
assert default_2.username == 'default_2' # The sequence is at 2
```

Above things worked out coincidentally. Twice FactoryBoy set the pk to the sequence value, but once
sqllite set the pk by autoincrement. It just so happened that the sequence was incremented at the same time. 

The above can get messy. The sequence is always the same (0, 1, 2), but, the pks are affected by what is already
in the database. So in a new shell, after a new import of the the factory class, the sequence starts over at
a predictable value. The pks start depends upon what is in the database. Also, if you can increment the database
pk without incrementing the factory sequence, you can get in trouble, in that the sequence will try to use a pk that 
already exists. Also, if you are hardcoding pks into this readme, those hardcodes assume that the database started at
0. The problem comes when the sequence is assigning pks, 
and the pk gets incremented without the sequence knowing about it. If the sequence is always in charge of the PK, that
is ok. But the minute another object gets created, the db autoincrements, but the sequence never changes, so 
the next up in the sequence has already been assigned.

```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

# reference the sequence from the child class
from factoryboy_example.example_factories import ExampleUserFactory_one_sequence
default_0 = ExampleUserFactory_one_sequence()
assert default_0.id == 0 # The sequence starts at 0
assert default_0.username == 'default_0' # The sequence starts at 0

# increment the pk, but not the sequence
from django.contrib.auth.models import User
tom = User(username='tom')
tom.save()

# and lets look at the squence from the child class
default_1 = ExampleUserFactory_one_sequence()
assert default_1.id == 1 # The sequence is at 1
assert default_1.username == 'default_1' # The sequence is at 1
```

does importing factory class reset the sequence? No.
Does restarting the shell reset the sequence? Yes.

#### Post Generation
Extracting arguments written as the Factory was Invoked (as in, I will invoke the factory, it will produce an object.)

https://factoryboy.readthedocs.io/en/stable/reference.html#inheritance

```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

from factoryboy_example.example_factories import UserFactory_PostGeneration
steve = UserFactory_PostGeneration.create(any_word_will_do__der="schüler", any_word_will_do__die="schülerin", any_word_will_do__article_die="schule")
```

I will write a factory s.t.
1) the pk and username are guaranteed to match
2) The sequence values are never used as primary keys
3) There is never a conflict where the factory tries to create an object that has a pk that already exists
4) Previously, if pks were set by the sequence, then if an object was created without the sequence knowing,
The sequence would not have the next valid pk.
   
In summary, lets not meddle with the primary key, let the dbengine manage the pk. 

```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

from factoryboy_example.example_factories import Unique
from django.contrib.auth.models import User
Unique(set_username="fred")
Unique()
tom = User(username='tom')
Unique(set_username="freed")
Unique()
Unique(set_username="fr")
```

#### build vs create

You can see that there is no id available with the build method.
a.id evaluates to None.

```
rm mysite/db.sqlite3
python mysite/manage.py migrate
python mysite/manage.py shell

from factoryboy_example.example_factories import Unique

a=Unique.build()
b=Unique.create()
c=Unique()

assert a.id == None
assert b.id == 1
assert c.id == 2    
```

#### Lazy Functions
Lazy Functions can be used to fill model fields.
I guess it is lazy in the sense that the function is not evaluated until the object is actually instantiated?
I guess you could say that the value for a LazyFunction field is decided at runtime.
Note that the username for this new user will be the default. It will clash with old users who got the same default.
```
from factoryboy_example.example_factories import ExampleUserFactory_lazyfunction
user_lazyfunction = ExampleUserFactory_lazyfunction()
# check the field that was generated using a lazy function
assert user_lazyfunction.password == 'default--from-lazy-function'
# check a default field
assert user_lazyfunction.username == 'default'
```

#### Lazy Attributes:
Lazy Attributes can be used to fill model fields, this time with Factory Defaults 
(Factory Defaults are those values written into the factory class definition.)
Lazy Attributes overwrite Factory Defaults if there is disagreement.
```
from factoryboy_example.example_factories import lazyattribute
user_lazyattribute = lazyattribute()
assert user_lazyattribute.password == 'lazy_pw'
assert user_lazyattribute.email == 'lazy_user@gmail.com'
user_lazyattribute.delete()
```

If the factory defaults are overwritten at Factory Invocation,
The Lazy Attribute references the new values rather than Factory Defaults.
```
from factoryboy_example.example_factories import lazyattribute
user_lazyattribute = lazyattribute(username='stephen')
assert user_lazyattribute.password == 'lazy_pw'
assert user_lazyattribute.email == 'stephen@gmail.com'
user_lazyattribute.delete()
```

LazyAttributes can be overwritten at Factory Invocation.
```
from factoryboy_example.example_factories import lazyattribute
user_lazyattribute = lazyattribute(email='stephen')
assert user_lazyattribute.password == 'lazy_pw'
assert user_lazyattribute.email == 'stephen'
user_lazyattribute.delete()
```

LazyAttributes can NOT reference themselves. 
You get a `CyclicDefinitionError`
```
from factoryboy_example.example_factories import lazyattribute_reflexive
user_lazyattribute = lazyattribute_reflexive()
assert user_lazyattribute.password == 'lazy_pw'
assert user_lazyattribute.email == 'lazy_email@gmail.com'
```

The id is assigned to the object after object instantiation, at database save.
The id is not available to the lazy attribute.
```
from factoryboy_example.example_factories import lazyattribute_id
user_lazyattribute = lazyattribute_id()
```
This fails with `AttributeError` because the id doesn't exist yet.
The attribute id is created after the object has been instantiated in the db.
It must be that the lazyattribute is computed before the db instantiation. 
The error message actually gives a list of attributes that can be evaluated. 

#### Non KWarg args:
[non KWarg args](https://factoryboy.readthedocs.io/en/stable/introduction.html#non-kwarg-arguments)
Normally,the fields of the Factory class have the name of the instantiated classes' kwargs.
You can give the fields of the Factory class their own name, and then construct a tuple
which will be used as the arguments to instantiate the class (the overall context here
is that we are using a factory class to instantiate another class, this other class
is what I mean when I say 'the class').
```
python mysite/manage.py shell
from factoryboy_example.example_factories import Mine
# instantiate the class with three positional arguments
mine = Mine(1, 2, 3)
assert mine.a == 1; assert mine.b == 2; assert mine.c == 3

from factoryboy_example.example_factories import MineFactory
# MineFactory passes a tuple of three positional arguments as the argument
# to instantiate the Mine Class. Note that the fields in the mine class, as
# well as the parameters for the init function, are called 'a', 'b', and 'c'.
# When we call the factory, we overwrite the MineFactory field 'second_position,
# which is in turn provided by MineFactory as the second positional argument to
# the class we are instantiating.
mine = MineFactory(second_position=33)
assert mine.a == 1; assert mine.b == 33; assert mine.c == 3
```

#### Parameters and Traits
[Code along for this section](https://factoryboy.readthedocs.io/en/stable/introduction.html#altering-a-factory-s-behavior-parameters-and-traits)

You can pass to a Factory a parameter which is then used by a LazyAttribute to calculate the actual fields of the
generated object. Recall that lazy attributes can compute object attributes/fields depending on values already
assigned to the object, in this way they are lazy.

A 'Rental' has a start and an end date:
```
python mysite/manage.py shell
import datetime
from factoryboy_example.example_factories import Rental
rental0 = Rental(datetime.datetime(2009, 1, 1), datetime.datetime(2010, 1, 1))
print(rental0.begin)
print(rental0.end)
```

The factory computes the end date based off of a random start date (a fuzzy date),
and the duration parameter.
```
python mysite/manage.py shell
from factoryboy_example.example_factories import RentalFactory
rental0 = RentalFactory(duration=19)
print(rental0.begin)
print(rental0.end)
```

If you have a group of attributes that you want set a certain way in certain situations, use traits.
```
python mysite/manage.py shell
from factoryboy_example.example_factories import RentalFactory
rental0 = RentalFactory(old=True)
print(rental0.begin)
print(rental0.end)
```

#### build vs. create
Does the factory save the item to the database?
```
python mysite/manage.py shell

from django.contrib.auth.models import User
print(f"{'len(User.objects.all()): '}{len(User.objects.all())}")
from factoryboy_example.example_factories import ExampleUserFactory
stephen = ExampleUserFactory(username='stephen', email='stephen@stephen.com')
print(f"{'len(User.objects.all()): '}{len(User.objects.all())}")
```

from django.contrib.auth.models import User

# Fixture with Module Scope

### Run commands 
```
cd fixture_with_module_scope
pytest
```

### Observe output

#### RIDDLE: 

Look at the output, you can see that the fixture was instantiated for module_1 and module_2, but not
module_3. Nevertheless, we see successful reads of fixture data for all three modules. How can that be?

#### EXPLANATION:

We use the tmpdir_factory fixture in two ways. The way they probably want you to use it, and an
under-the-hood way.

In `fixture_with_module_scope/conftest.py::module_file` we use the `mktemp()` and `join()`
methods of the tmpdir_factory to generate a file object.
We modify the file and then return it. Since that file is the return value of a function decorated
as a fixture, it is now the value for a fixture which has the same name as the original function, and
is available to other tests. Since we designated this fixture to have a module wide scope, a new object
will be generated for each module. The new fixture is called `module_file` and is consumed in 
modules 1 and 2 as a fixture.

In the output from the `pytest` call, observe that the fixture setup function 
for the fixture (`fixture_with_module_scope/conftest.py::module_file`)
is executed twice, once for module 1 and once for module 2. 

We also use the tmpdir_factory in an under-the-hood way. Instead of consuming the published fixture (which obeys
the scope rules we defined in the decorator), we can get directly the directory where the
fixture file is stored from tmpdir_factory. We do this in `fixture_with_module_scope/test_module_3::test_5`.
Note that we successfully read the information that was stored in the first instantiation
of the `module_file` fixture (if you look at the timestamps), and that no setup function was run
for the third module, despite the scope rules we defined for the fixture.
(There is a time recorded for fixture instantiation for module 1 and module 2, but not module 3)

Short Answer: The fixture consumed in module_3 is scoped to the session, and has access to the data that was
generated in the setup call used to create the module-scoped custom fixtures.1

# Module Caching

This example is companion code to the
[fixtures-can-be-requested-more-than-once-per-test-return-values-are-cached]
(https://docs.pytest.org/en/6.2.x/fixture.html#fixtures-can-be-requested-more-than-once-per-test-return-values-are-cached)
section of the pytest documentation


## Run these commands

```
cd module_cache
pytest
```

## Observe output

Observe the following:

- two tests run, `test_1` and `test_2`.
- For `test_1`, during setup, all three fixture functions were called.
- For `test_2`, there was no setup, despite `test_2` using the same fixtures.
- The id of the fixture named `append` is the same in both tests.

We can see that the fixtures were cached.
They were scoped to the module, then they were called ONLY ONCE.

# Autouse

This example is companion code to the
[https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request](autouse)
section of the pytest documentation

## Run these commands

```
cd autouse
pytest
```

## Observe output and code

Observe the following:

- two tests run, `test_1` and `test_2`.
- Despite neither test calling the append0 fixture, the list0 fixture has been modified for the body of the test.

# scope sharing fixtures across classes modules packages or session
This is the code-along for the
[Scope: sharing fixtures across classes..](https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session)
section of the documentation.

This section also considers a discussion of the output that pytest provides, how the output reflects fixture
scoping, and how pytest recoginizes same-named tests in different modules as distinct.

## Run 

```
pytest scope__sharing_fixtures_across_classes
```

## Observe

The tests fail for demo purporses. 
When tests fail in pytest,
output is printed to the console. 
There is a section of output for each test that failed.

Each section contains
- a list of fixtures requested by the test
- the test defintion
- 'Captured stdout setup' (if stdout was captured during setup)
- 'Captured stdout call' (if stdout was captured during 'call', the actual execution of the test)

Note that five tests are defined across two modules.
Module 1 contains test_1 and test_2. 
Module 2 contains test_1, test_2, and test_2.
In this example, four tests are discovered and executed.

Note that the module name is not printed to the output, only the test name. Despite this, tests
of the same name but in different modules are considered distinct tests.

Let us examine the output for test__module_1::test_1.

- Two fixtures are printed. For the smpt connection,
the print method returns an unfamiliar looking thing with a memory address. 
For the fixture `dict0`, the actual dictionary is printed.
  
- The test definition is printed, with the failing line highlighted.

- Stdout was captured during setup - this is printed. In this case it happens to be a print statement executed
durint instantiation of a module based fixture called 'smpt_connection'.
  
- Stdout was captured from the actual execution of the test.

Let us compare this to the output for the sister-test, test__module_1::test_2.

- only 1 fixture was requested; it is the smtp connection object, and it is printed.
 
- No stdout was captured during setup for this test - this is because the fixture which this test requested
was scoped to the module, and a test in this module had already requested the fixture, so the fixture object
was available in the cache. 

# Scope 0   

## Run these commands

```
cd autouse
pytest
```

## Examine code, Observe output and code

This module has two tests - the first passes and then the second fails, despite the tests
being identical. 

How does this happen in this case?

There is an autouse fixture which modifies a module-scoped fixture. The two tests
check the content of this module-scoped fixture, which happens to be modified during setup
of both of the tests. The first test runs and the module-scoped fixture looks like it should
look, and then the second tests setups, and the autouse fixture then modifies the
module scoped fixture. Then of course the second test fails. 

# Fixture Errors

This is the code-along for the 
[fixture errors section](https://docs.pytest.org/en/6.2.x/fixture.html#fixture-errors)
of the pytest documentation.

## run

```
cd fixture_errors
pytest
```

## observe

For each file, the test does not explicitly declare usage of the fixtures called
'first' 'second' and 'third'. The 'third' fixture is an autouse fixture,
so it is made available to the test. It has as a dependency the second fixture, so 
the second fixture runs prior to the third, and the 'first' fixture is a dependency 
to the second fixture, so it runs first. 

For test_1, three fixture setup functions run, and there is an error during the setup for the
third fixture. The standard out for all fixture functions is captured.

For test_2, only two fixture setup functions run, because there is an error
during the setup for the second fixture. 
The standard out for the first two setup functions is captured, but not for the third.

For test_3, ony 1 fixture setup function runs, because there is an error during the
setup for the first fixture. 
The standard out for only the first setup function is captured.

# Fixture Availability
1. [fixture availability]

This is the code-along for the 
[fixture availability](https://docs.pytest.org/en/6.2.x/fixture.html#fixture-availability)
section of the pytest documentation.

## Run

```
cd fixture_errors
pytest test_1.py test_2.py
```

## Observe
All the tests pass, nothing interesting about the output.
Read the comments in the code for a walk-through of how fixture definitions
are discovered.

## Run

```
cd fixture_errors
pytest test_3.py
```

## Observe
Test_0 fails, because it cannot find the fixture it is requesting. The fixture is defined
at a smaller scope, or a more local scope, or you could say a lower scope. Test_0 is 
defined in the global namespace, it can only see up, it cannot see down (if you will)
into the smaller scope. 

Test_1 passes, it can find the fixture, because the fixture is defined in the same scope
as the test. (it has to be the same scope or above).

Note that the fixture is scoped to the session! The highest and most global scope you can
assign to a fixture. Welll ... what? The answer is, there is a difference between
fixture availability and the scope in which the fixture is instantiated and cached.
More concretely, the scope argument of the fixture decorator determines 'fixture sharing',
while the placement in the text file (how indented it is), defines availability.  

# conftest.py: sharing fixtures across multiple files 

This is the code-along for the 
[conftest.py: sharing fixtures across multiple files](https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files)
of the pytest documentation.

## Run

```
cd sharing_fixtures/1
pytest 
```

## Observe

- The tests fail, but only because of some assert 0 statements. 

- If you read the output in the terminal, you see that there are two distinct
tests collected, even though these two tests have the same name. This is 
ok because the tests are in different modules (files).
  
- Observe in the output that both tests request the same fixture (list0), 
but that the fixture takes on different values in either test.
Specifically, the name of the file (module) is written into the fixture. 

- The tests in the two test files in this directory (or the two test modules
in this package, if you will) are able to 'see' the fixture they are requesting,
because this fixture is written into the package conftest and is therefore visible to
every test in the package. You could say this fixture is defined in the package scope,
or that the fixture is defined in the package (folder) namespace  
Note that this fixture has module scope (scope in the sense of sharing, not visibility),
so a new fixture (which in this case is a list) is created for each file.
The fixture is defined in a package scope (it is written into a conftest). 
The fixture has             module scope (it will be instantiated once for each module).  

- The tests add 1 thing to the fixture, and then assert that is the only thing in the fixture. 
Since the fixture is scoped to the module, it is found to be true that no other logic tampered
with the instantiated fixture. 

## Run

```
cd sharing_fixtures/2
pytest 
```

## Observe

This is exactly the same as 1/, except the fixture (written in a place where
it is visible to the entire package) is scoped per package, rather than the
default function. This makes the tests fail, as each test only expects
to see the content that it added. 

# higher-scoped-fixtures-are-executed-first
this is the code-along for the
[higher-scoped-fixtures-are-executed-first](https://docs.pytest.org/en/6.2.x/fixture.html#higher-scoped-fixtures-are-executed-first)
section of the pytest documentation

## Run

```
pytest fixture_ordering 
```

## Observe
There are two modules (files) in this test package (directory).

test_module_1.py demonstrates that larger (or higher) scoped fixtures are executed first. 

test_module_2.py demonstrates a `ScopeMismatch` error - you cannot scope a fixture the to function, 
and then request it in a `session` scoped fixture. How would that even work - the session scope fixture
has setup code only run 1 time for it and thten it is cached, but if you tried to access a function scoped
fixture with it, then you would need to run setup for the session scoped object for each function. Requesting
a fixture sort of parametrizes your fixture on that other fixture. If that other fixture varies function to function,
well then so does your current fixture (varying function to function is emphatically not a session scope)a
```
ScopeMismatch: You tried to access the 'function' scoped fixture 'order' with a 'session' scoped request object, involved factories
```


# running-multiple-assert-statements-safely
This is the code-along for the
[running-multiple-assert-statements-safely](https://docs.pytest.org/en/6.2.x/fixture.html#running-multiple-assert-statements-safely)
section of the documentation.

lets say you have many setup steps, and you then you want to run multiple assert statements.

If you run all the assert statements immediatly after setup, then if one fails, the other asserts will not run
and you will lose all the work that was done for setup.

The recommended pattern is to create a class for this situation, where the setup work is done in an autouse fixture
scoped to the larger class scope (scoping, repeatability), and situated in the larger class scope (discoverability). 
Each assert statement is a function which exists in the class scope, and which can therefore target (can see)
the setup logic. We are assured that the setup logic only runs once, because the setup logic is scoped to the class,
and all the assert statements exist in the class.

## Run

```
pytest multiple_assert 
```

Remember that pytests follows a philosophy or theme of
[Arrange, Act, Assert, Cleanup](https://docs.pytest.org/en/6.2.x/fixture.html#what-fixtures-are)
when it comes to running a test. 

## Observe

The 'act' logic ran only once. (in the output, you see 'running act logic', only 1 time)

We know exactly which assert statements failed (asserts 1, 3) and which succeeded (asserts 0, 2,3).

Had we not followed this class based pattern where the "act logic" (official pytest term) was placed in
a class, scoped to that class, and marked as autouse, we would not have known which tests failed and which
tests passed. 

The 'act' step is autouse - this guarantees it runs after the 'arrange' step, which is not auto-use. This also
guarantees that the 'act' logic will run before all the tests, and since the act logic has been scoped to the class, 
we can see that it will run only once.

# fixtures-can-introspect-the-requesting-test-context

This is the code-along for the 
[fixtures-can-introspect-the-requesting-test-context](https://docs.pytest.org/en/6.2.x/fixture.html#fixtures-can-introspect-the-requesting-test-context)
section of the pytest documentation.

## Run

```
pytest fixtures-can-introspect
```

## Observe

Note that each module has a failing test and a passing test. 

Even though the passing tests (which are in different modules) use the same fixture, the smtp connection is 
to different servers.

The passing tests use fixtures which are scoped to the function. Stdout was captured during setup of these tests
that shows the name of the requesting function, 
the name of the module from where the request originated, 
and the list of variables available in the module namespace. 

The failing tests use fixtures which are scoped to the module. The fixtures error during setup, which is recorded
explicitly in the error message with the heading "ERROR at setup of test_2". The actual error message is:

`AttributeError: function not available in module-scoped context`

The fixture tries to request the function name from the request object (the request object holds information 
about the requesting test). There was a function that requested this fixture - that is why this fixture logic
is running. Why is the function not available? There are many ways that the authors/developers could have set this up,
but one way you could probably think of it as the function name is in that request object, but the author of the test
is forbidden to reference it given that the fixture has been scoped to the module. If the fixture is scoped to the
module, then references to function scoped fields in the request object will generate an AttributeError. If this 
were not the case, then you might run into a problem where the fixture which is used by a test is parametrized by 
a different function's name, because the other function triggered the fixture to be instantiated and then cached. 

You can make a function (test) aware of its name using this technique. Scope a fixture to the function, have it 
extract from the request objec the name of the function (test) which requested it, and then return that name as 
the fixture value. You can't really do this in Python, in part because its not that useful. 


# Match Error Messages
This file demonstrates how to write tests which expects certain Errors and Exceptions.
Moreover, with pytest you can demand specific error messages of your tests.

```
pytest exceptions.py
```


### Apendix
```
npm install markdown-toc
npx markdown-toc README.md
```
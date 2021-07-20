# Index 

### Initialization
1. [Initialization](#initialization)

### Plugins

1. [pytest django 0](#pytest-django-0)
1. [pytest django 1](#pytest-django-1)
1. [factoryboy](#factoryboy)

### Fixtures
1. [fixture with module scope](#fixture-with-module-scope)
1. [module caching](#module-caching)
1. [scope 0](#scope-0)   
1. [autouse](#autouse)
1. [scope: sharing fixtures across classes modules packages or session](#scope-sharing-fixtures-across-classes-modules-packages-or-session)
1. [fixture errors](#fixture-errors)
1. [fixture availability](#fixture-availability)
1. [conftest.py: sharing fixtures across multiple files](#conftestpy-sharing-fixtures-across-multiple-files)
1. [higher-scoped-fixtures-are-executed-first](#higher-scoped-fixtures-are-executed-first)
1. [running-multiple-assert-statements-safely](#running-multiple-assert-statements-safely)
1. [#fixtures-can-introspect-the-requesting-test-context](#fixtures-can-introspect-the-requesting-test-context)




# Initialization

```
python3 -m venv testenv
source testenv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

# pytest django 0
thi is the code along for the
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


#factoryboy
This is the code-along for the
[basic usage section](https://factoryboy.readthedocs.io/en/stable/introduction.html#basic-usage)
of the factoryboy plugin.

I want to instantiate a User. 
I want that User to have default configuration. 
I will provide only the first name and last name.

```
python mysite/manage.py shell
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


default = ExampleUserFactory()
# Check Default fields
default.username == 'default'
default.password == 'default'
default.is_superuser == True
default.is_staff == True
default.email == 'default'
```

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
[fixtures-can-be-requested-more-than-once-per-test-return-values-are-cached](https://docs.pytest.org/en/6.2.x/fixture.html#fixtures-can-be-requested-more-than-once-per-test-return-values-are-cached)
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

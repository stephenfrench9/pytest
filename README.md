# Index

1. [Initialization](#initialization)
1. [fixture with module scope](#fixture-with-module-scope)
1. [module caching](#module-caching)
1. [scope 0](#scope-0)   
1. [autouse](#autouse)
1. [fixture errors](#fixture-errors)
1. [fixture availability](#fixture-availability)
1. [conftest.py: sharing fixtures across modules (files)](#conftestpy-sharing-fixtures-across-multiple-files)

# Initialization

```
python3 -m venv testenv
source testenv/bin/activate
python -m pip install -r requirements.txt
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

# conftestpy sharing fixtures across multiple files 

This is the code-along for the 
[conftest.py: sharing fixtures across files (modules)](https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files)
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

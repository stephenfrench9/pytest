## Initialize

```
python3 -m venv testenv
source testenv/bin/activate
python -m pip install -r requirements.txt
```

[What you see](#test)

## Fixture with Module Scope

### Run commands 

```
cd fixture_with_module_scope
pytest
```

### Observe output

#### RIDDLE: 

Look at the output, you can see that the fixture was instantiated for module_1 and module_2, but not
module_3. Nevertheless, we see successful reads of fixture data for all three modules. How can that be?

#### test

anythin

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
generated in the setup call used to create the module-scoped custom fixtures.
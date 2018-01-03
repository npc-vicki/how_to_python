import stuff

def inline_stuff():
    return 'things'

def test_inline_stuff():
    assert inline_stuff() == 'things'

def test_imported_stuff():
    assert stuff.imported_stuff() == 'things'

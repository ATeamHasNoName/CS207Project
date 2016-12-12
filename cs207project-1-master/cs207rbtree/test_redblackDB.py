from redblackDB import connect
import os

def gen_demo_data():
    # initialize database
    db = connect("DELETEME.dbdb")
    db.close()

    # fill database
    input_data = [
        (1,"one"), 
        (3,"three"),
        (4,"four"),
        (6,"six"),
        (7,"seven"),
        (8,"eight"),
        (10,"ten"),
        (10,"ten"),
        (13,"thirteen"),
        (14,"fourteen"),
        ]
    db = connect("DELETEME.dbdb")
    for key, val in input_data:
        db.set(key, val)
    # db._print_tree() # USE THIS TO VISUALIZE TREE
    db.commit()
    db.close()

def purge_demo_data():
    try: 
        os.remove("DELETEME.dbdb")
    except:
        pass

def test_balance_successful():
    gen_demo_data()
    # check balance
    # note that in the absence of balancing every node will be entered to the right
    db = connect("DELETEME.dbdb")
    assert db.get_left(6)==(3,"three")
    assert db.get_right(6)==(8,"eight")
    assert db.get_left(3)==(1,"one")
    assert db.get_right(3)==(4,"four")
    assert db.get_left(8)==(7,"seven")
    assert db.get_right(8)==(13,"thirteen")
    assert db.get_left(13)==(10,"ten")
    assert db.get_right(13)==(14,"fourteen")
    db.close()
    purge_demo_data()

def test_get_min():
    gen_demo_data()
    db = connect("DELETEME.dbdb")
    assert db.get_min()=="one"
    db.close()
    purge_demo_data()

def test_chop_on_key_in_db():
    gen_demo_data()
    db = connect("DELETEME.dbdb")
    assert db.chop(6)==[(6, u'six'), (1, u'one'), (3, u'three'), (4, u'four')]
    db.close()
    purge_demo_data() 

def test_chop_on_key_not_in_db():
    gen_demo_data()
    db = connect("DELETEME.dbdb")
    assert db.chop(6.1)==[(6, u'six'), (1, u'one'), (3, u'three'), (4, u'four')]
    db.close()
    purge_demo_data() 

def test_commit_necessary():
    gen_demo_data()
    db = connect("DELETEME.dbdb")
    db.set(10, "nonsense") # this fails
    db.close()

    db = connect("DELETEME.dbdb")
    assert db.get(10)=="ten"
    db.close()

    db = connect("DELETEME.dbdb")
    db.set(10, "nonsense") # this works
    db.commit()
    db.close()

    db = connect("DELETEME.dbdb")
    assert db.get(10)=="nonsense"
    db.close()
    purge_demo_data() 



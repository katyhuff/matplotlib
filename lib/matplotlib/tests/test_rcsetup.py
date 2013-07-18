import os

import matplotlib as mpl
from matplotlib.tests import assert_str_equal
from StringIO import StringIO

matplotlibrc = os.path.join(os.path.dirname(__file__), 'matplotlibrc.template')
templaterc = os.path.join(os.path.dirname(__file__), '../test_rcsetup.rc')
deprecated = ['svg.embed_char_paths', 'savefig.extension']

rc_file = StringIO()
f = open(matplotlibrc)
for line in f :
    modified = line.replace("^#([^ ])", "\1")
    if modified.count("datapath") == 0 : 
        rc_file.write(modified)

def test_defaults():
    # the default values should be successfully set by this class
    with mpl.rc_context(rc=mpl.rcsetup.defaultParams):
        for k, v in mpl.rcsetup.defaultParams.iteritems():
            if k not in deprecated:
                assert mpl.rcParams[k][0] == v[0]


def test_template():
    # the current matplotlibrc.template should validate successfully
    with mpl.rc_context(fname=rc_file):
        for k, v in mpl.rcsetup.defaultParams.iteritems():
            if k not in deprecated:
                if isinstance(v[0], basestring):
                    assert mpl.rcParams[k] in [v[0], v[0].lower()]
                else : 
                    assert mpl.rcParams[k] == v[0]

def test_unicode():
    # unicode formatted valid strings should validate successfully
    for k, v in mpl.rcsetup.defaultParams.iteritems():
        if k not in deprecated:
            if isinstance(v[0], basestring):
                u = v[1](unicode(v[0]))
                if u not in [v[0], v[0].lower()] :
                    print "Expected : ", v[0]
                    print "Actual : ", u
                assert u in [v[0], v[0].lower()]


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)

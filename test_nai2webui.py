from nai2webui import nai2webui

def test_escape_parentheses():
    assert nai2webui('cat (animal)') == 'cat \\(animal\\)'


def test_plain_cat():
    assert nai2webui('cat') == 'cat'


def test_1_05_cat():
    assert nai2webui('{cat}') == '(cat:1.05)'


def test_1_10_cat():
    assert nai2webui('{{cat}}') == '(cat:1.10)'


def test_masterpiece_1_05_cat():
    assert nai2webui('masterpiece {cat}') == 'masterpiece (cat:1.05)'


def test_0_95_cat():
    assert nai2webui('[cat]') == '(cat:0.95)'


def test_1_05_cat_and_plain_dog():
    assert nai2webui('{cat} and dog') == '(cat:1.05) and dog'


def test_1_05_cat_and_1_00_dog():
    assert nai2webui('{cat and [dog]}') == '(cat and (dog:0.95):1.05)'

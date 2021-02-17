#!/usr/bin/env python

import pytest
from DictOfContainers import DictOfContainers

@pytest.fixture
def int_dict_of_dict():
    return DictOfContainers({1: {2: 3}, 4: {5: 6, 7: 8, 9: 10}})

@pytest.fixture
def dict_with_empty_dict():
    return DictOfContainers({1: {2: 3}, 4: {5: 6, 7: 8}, 9: {10: 11}, 12: {}})

@pytest.fixture
def string_dict_of_dict():
    return DictOfContainers({'hello': {'world': '42'}})

@pytest.fixture
def empty_dict_of_dict():
    return DictOfContainers({})

@pytest.fixture
def mixed_dict():
    return DictOfContainers({1: [2, 3], 4: {5: 6}, 7: {8}})

# ---------------------------


def test_empty_value(dict_with_empty_dict):
    assert len(dict_with_empty_dict) == 3


def test_len(int_dict_of_dict):
    assert len(int_dict_of_dict) == 2


def test_empty_len(empty_dict_of_dict):
    assert len(empty_dict_of_dict) == 0


def test_outer_obj(int_dict_of_dict):
    assert int_dict_of_dict[1]._outer_obj is int_dict_of_dict


def test_delete(string_dict_of_dict):
    del string_dict_of_dict['hello']['world']
    assert len(string_dict_of_dict) == 0


def test_update(int_dict_of_dict):
    int_dict_of_dict.update({4: {5: 6}})
    assert int_dict_of_dict[4] == {5: 6}


def test_type(string_dict_of_dict):
    assert isinstance(string_dict_of_dict['hello'], dict)


def test_outer_clear(string_dict_of_dict):
    string_dict_of_dict.clear()
    assert len(string_dict_of_dict) == 0


def test_inner_clear(int_dict_of_dict):
    int_dict_of_dict[4].clear()
    assert len(int_dict_of_dict) == 1


def test_keys(int_dict_of_dict):
    assert set(int_dict_of_dict.keys()) == {1, 4}


def test_values(int_dict_of_dict):
    assert list(int_dict_of_dict.values()) == [{2: 3}, {5: 6, 7: 8, 9: 10}]


def test_outer_pop(int_dict_of_dict):
    int_dict_of_dict.pop(1)
    assert len(int_dict_of_dict) == 1


def test_inner_pop(string_dict_of_dict):
    string_dict_of_dict['hello'].pop('world')
    assert len(string_dict_of_dict) == 0


def test_default_pop(mixed_dict):
    mixed_dict[1].pop()
    mixed_dict[1].pop()
    assert len(mixed_dict) == 2

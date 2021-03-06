#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Descriptors for energy profile line classes.
"""

import numpy as np

from catplot.chem_parser import RxnEquation


class DescriptorBase(object):
    """ Abstract base class for other descriptor class.
    """
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        try:
            return instance.__dict__[self.name]
        except KeyError:
            msg = "{} object has no attribute {}".format(instance, self.name)
            raise AttributeError(msg)

    def __set__(self, instance, value):
        self._check(instance, value)
        instance.__dict__[self.name] = value

    def _check(self, instance, value):
        """ Just a placeholder.
        """


class ElementaryEnergies(DescriptorBase):
    """ Descriptor class for elementary energies for different state.
    """
    def __init__(self, name):
        super(ElementaryEnergies, self).__init__(name)

    def _check(self, instance, value):
        """ Check elementary energies validity.
        """
        if len(value) == 3:
            e_is, e_ts, e_fs = value
            if e_ts <= max(e_is, e_fs):
                raise ValueError("abnormal energies: {}".format(value))


class ElementaryReaction(DescriptorBase):
    """ Descriptor for elementary reaction.
    """
    def __init__(self, name):
        super(ElementaryReaction, self).__init__(name)

    def _check(self, instance, value):
        """ Check reaction validity.
        """
        if value is None:
            return

        rxn_equation = RxnEquation(value)

        if len(rxn_equation.tolist()) != len(instance.energies):
            msg = "Reaction length is not equal to the energies length"
            raise ValueError(msg)


class InterpolationMethod(DescriptorBase):
    """ Descriptor for interpolation algorithm.
    """
    def __init__(self, name):
        super(InterpolationMethod, self).__init__(name)

    def _check(self, instance, value):
        candidates = ["spline", "quadratic"]
        if value not in candidates:
            raise ValueError("inter)p_method must be one of {}.".format(candidates))


class MarginRatio(DescriptorBase):
    """ Descriptor for canvas margin ratio.
    """
    def __init__(self, name):
        super(MarginRatio, self).__init__(name)

    def _check(self, instance, value):
        if value <= 0.0 or value > 1.0:
            raise ValueError("margin ratio must be in (0, 1]")


class Coordinate2D(DescriptorBase):
    """ Descriptor for node in 2D grid.
    """
    def __init__(self, name):
        super(Coordinate2D, self).__init__(name)

    def _check(self, instance, value):
        if len(value) != 2 or not all([isinstance(entry, float) for entry in value]):
            raise ValueError("Invalid 2D coordinate: {}".format(value))


class Coordinate3D(DescriptorBase):
    """ Descriptor for node in 3D grid.
    """
    def __init__(self, name):
        super(Coordinate3D, self).__init__(name)

    def _check(self, instance, value):
        if len(value) != 3 or not all([isinstance(entry, float) for entry in value]):
            raise ValueError("Invalid 3D coordinate: {}".format(value))


class Basis2D(DescriptorBase):
    """ Descriptor for basis in 2D space.
    """
    def __init__(self, name):
        super(Basis2D, self).__init__(name)

    def _check(self, instance, value):
        if value.shape != (2, 2) or np.linalg.matrix_rank(value) != 2:
            raise ValueError("{} is not a valid 2D basis")


class Basis3D(DescriptorBase):
    """ Descriptor for basis in 3D space.
    """
    def __init__(self, name):
        super(Basis3D, self).__init__(name)

    def _check(self, instance, value):
        if value.shape != (3, 3) or np.linalg.matrix_rank(value) != 3:
            raise ValueError("{} is not a valid 3D basis")


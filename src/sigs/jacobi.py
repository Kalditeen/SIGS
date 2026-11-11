"""Jacobi elliptic function support for symbolic and numerical screening.

SymPy in this environment does not expose ``JacobiSN/CN/DN``, so this module
provides minimal ``sympy.Function`` subclasses with the correct first-argument
derivatives, a NumPy backend backed by ``scipy.special.ellipj``, and JAX
primitives with exact first-argument JVPs.  The elliptic modulus ``m`` is
treated as a fixed constant on the JAX path; symbolic back-substitution can
still promote the numeric seed modulus to a free parameter.
"""

from __future__ import annotations

import numpy as np
import scipy.special as sc
import sympy as sp

import jax
import jax.numpy as jnp


class JacobiSN(sp.Function):
    nargs = 2

    def fdiff(self, argindex):
        if argindex == 1:
            z, m = self.args
            return JacobiCN(z, m) * JacobiDN(z, m)
        return sp.Derivative(self, self.args[1])


class JacobiCN(sp.Function):
    nargs = 2

    def fdiff(self, argindex):
        if argindex == 1:
            z, m = self.args
            return -JacobiSN(z, m) * JacobiDN(z, m)
        return sp.Derivative(self, self.args[1])


class JacobiDN(sp.Function):
    nargs = 2

    def fdiff(self, argindex):
        if argindex == 1:
            z, m = self.args
            return -m * JacobiSN(z, m) * JacobiCN(z, m)
        return sp.Derivative(self, self.args[1])


SYMPY_LOCALS = {
    "JacobiSN": JacobiSN,
    "JacobiCN": JacobiCN,
    "JacobiDN": JacobiDN,
}


def _np_sn(u, m):
    return sc.ellipj(np.asarray(u), np.asarray(m))[0]


def _np_cn(u, m):
    return sc.ellipj(np.asarray(u), np.asarray(m))[1]


def _np_dn(u, m):
    return sc.ellipj(np.asarray(u), np.asarray(m))[2]


def _np_sech(u):
    return 1.0 / np.cosh(np.asarray(u))


NUMPY_MODULES = [
    {"JacobiSN": _np_sn, "JacobiCN": _np_cn, "JacobiDN": _np_dn, "sech": _np_sech},
    "numpy",
]


def reduce_jacobi_powers(expr):
    """Reduce cn**n and dn**n (n >= 2) to polynomials in sn.

    The Jacobi identities cn**2 = 1 - sn**2 and dn**2 = 1 - m*sn**2 turn an
    otherwise over-complete basis into ``sn**k * cn**eps * dn**delta`` with
    eps, delta in {0, 1}.  Coefficients extracted on this basis are the actual
    algebraic constraints for cnoidal PDE solutions.
    """

    def _target(e):
        return (
            isinstance(e, sp.Pow)
            and e.base.func in (JacobiCN, JacobiDN)
            and e.exp.is_Integer
            and e.exp >= 2
        )

    def _rewrite(e):
        base = e.base
        n = int(e.exp)
        z, m = base.args
        if base.func is JacobiCN:
            square = 1 - JacobiSN(z, m) ** 2
        else:
            square = 1 - m * JacobiSN(z, m) ** 2
        if n % 2 == 0:
            return square ** (n // 2)
        return base * square ** ((n - 1) // 2)

    return sp.expand(expr.replace(_target, _rewrite))


def _ellipj_component(u, m, component):
    return float(sc.ellipj(float(u), float(m))[component])


def _jax_callback(u, m, component):
    return jax.pure_callback(
        lambda a, b: _ellipj_component(a, b, component),
        jax.ShapeDtypeStruct((), jnp.float64),
        u,
        m,
        vmap_method="sequential",
    )


@jax.custom_jvp
def jax_sn(u, m):
    return _jax_callback(u, m, 0)


@jax.custom_jvp
def jax_cn(u, m):
    return _jax_callback(u, m, 1)


@jax.custom_jvp
def jax_dn(u, m):
    return _jax_callback(u, m, 2)


@jax_sn.defjvp
def _jax_sn_jvp(primals, tangents):
    u, m = primals
    udot, _mdot = tangents
    return jax_sn(u, m), jax_cn(u, m) * jax_dn(u, m) * udot


@jax_cn.defjvp
def _jax_cn_jvp(primals, tangents):
    u, m = primals
    udot, _mdot = tangents
    return jax_cn(u, m), -jax_sn(u, m) * jax_dn(u, m) * udot


@jax_dn.defjvp
def _jax_dn_jvp(primals, tangents):
    u, m = primals
    udot, _mdot = tangents
    return jax_dn(u, m), -m * jax_sn(u, m) * jax_cn(u, m) * udot

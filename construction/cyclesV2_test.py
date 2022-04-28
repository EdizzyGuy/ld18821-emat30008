import sys
import os
origin = r'C:\\Users\\Ediz\\Documents\\uni stuff\\Scientific Computing\Assignment\\ld18821-emat30008'
sys.path.append(origin)

import numpy as np
import time
from ode import solve_ode
from scipy.integrate import solve_ivp
from scipy.optimize import root, fsolve
from numerical_continuationV1 import find_limit_cycles as cycles1
from numerical_continuationV2 import find_limit_cycles as cycles2
from numerical_continuationV2 import shooting

''' THIS CODE CONFIRMS THAT NO PERFORMANCE HAS BEEN LOST WITH V2

V1_times
[0.5483455657958984, 1.2935547828674316, 1.1830687522888184, 1.9880702495574951]
V2_times
[0.5162813663482666, 0.5537970066070557, 1.1752848625183105, 1.1912851333618164]
'''

PI = np.pi
solver_args={'deltat_max' : 0.01}
init_cond = np.array([1,1])
#np.random.normal(size=2) * 9
period_guess = np.random.uniform(low=5, high=25, size=1)
init_hopf = np.concatenate((init_cond, period_guess))

init_cond = np.array([1,1,1])
init_hopf_ext = np.concatenate((init_cond, period_guess))

def hopf_bifurcation(t, U, beta, sigma):
    u1 = U[0]
    u2 = U[1]

    u1_dot = beta*u1 - u2 + sigma *u1 *(u1*u1 + u2*u2)
    u2_dot = u1 + beta*u2 + sigma *u2 *(u1*u1 + u2*u2)
    U_dot = np.array([u1_dot, u2_dot])
    return U_dot

def hopf_extended(t, U, beta=2, sigma=-1):
    t = None

    U_dot = np.zeros(3)
    U_dot[:-1] = hopf_bifurcation(t, U[:-1], beta, sigma)
    U_dot[-1] = - U[-1]

    return U_dot

def test_shooting_hopf_scipySolver():
    beta, sigma = 2,-1
    atol, rtol = 1e-2, 1e-2
    # from analytical solution
    anal_period = 2* PI
    anal_radius = np.sqrt(beta)

    roots = cycles2(hopf_bifurcation, init_hopf, args=(beta, sigma))
    #find_limit_cycles(hopf_bifurcation, init_guess, args=(beta, sigma))
    numer_period = roots[-1]
    numer_radius = np.linalg.norm(roots[:-1])

    # check if period is a multiple of the analytical sol
    period_multiplicity = numer_period / anal_period
    period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
    print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
    print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
    return

def test_shooting_hopf_mySolver():
    beta, sigma = 2,-1
    atol, rtol = 1e-2, 1e-2
    # from analytical solution
    anal_period = 2* PI
    anal_radius = np.sqrt(beta)

    roots = cycles2(hopf_bifurcation, init_hopf, solve_ode, args=(beta, sigma))
    #find_limit_cycles(hopf_bifurcation, init_guess, args=(beta, sigma))
    numer_period = roots[-1]
    numer_radius = np.linalg.norm(roots[:-1])

    # check if period is a multiple of the analytical sol
    period_multiplicity = numer_period / anal_period
    period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
    print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
    print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
    return

def test_shooting_hopf_ext_scipySolver():
    beta, sigma = 2,-1
    atol, rtol = 1e-2, 1e-2
    # from analytical solution
    anal_period = 2* PI
    anal_radius = np.sqrt(beta)

    roots = cycles2(hopf_extended, init_hopf_ext, args=(beta, sigma))
    numer_period = roots[-1]
    numer_radius = np.linalg.norm(roots[:-1])

    # check if period is a multiple of the analytical sol
    period_multiplicity = numer_period / anal_period
    period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
    print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
    print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
    return

def test_shooting_hopf_ext_mySolver():
    beta, sigma = 2,-1
    atol, rtol = 1e-2, 1e-2
    # from analytical solution
    anal_period = 2* PI
    anal_radius = np.sqrt(beta)

    roots = cycles2(hopf_extended, init_hopf_ext, solve_ode, args=(beta, sigma))
    numer_period = roots[-1]
    numer_radius = np.linalg.norm(roots[:-1])

    # check if period is a multiple of the analytical sol
    period_multiplicity = numer_period / anal_period
    period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
    print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
    print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
    return


V2_times = []

start = time.time()
test_shooting_hopf_scipySolver()  # true
end  = time.time()
V2_times.append(end - start)

start = time.time()
test_shooting_hopf_mySolver()  # true
end  = time.time()
V2_times.append(end - start)

start = time.time()
test_shooting_hopf_ext_scipySolver()  # true
end  = time.time()
V2_times.append(end - start)

start = time.time()
test_shooting_hopf_ext_mySolver()  # true
end  = time.time()
V2_times.append(end - start)


def hopf_scipySolver():
    beta, sigma = 2,-1
    atol, rtol = 1e-2, 1e-2
    # from analytical solution
    anal_period = 2* PI
    anal_radius = np.sqrt(beta)

    roots = cycles1(hopf_bifurcation, init_hopf, solve_ivp, args=(beta, sigma))
    numer_period = roots[-1]
    numer_radius = np.linalg.norm(roots[:-1])

    # check if period is a multiple of the analytical sol
    period_multiplicity = numer_period / anal_period
    period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
    print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
    print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
    return

def hopf_mySolver():
    beta, sigma = 2,-1
    atol, rtol = 1e-2, 1e-2
    # from analytical solution
    anal_period = 2* PI
    anal_radius = np.sqrt(beta)

    roots = cycles1(hopf_bifurcation, init_hopf, args=(beta, sigma))
    numer_period = roots[-1]
    numer_radius = np.linalg.norm(roots[:-1])

    # check if period is a multiple of the analytical sol
    period_multiplicity = numer_period / anal_period
    period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
    print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
    print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
    return

def hopf_ext_scipySolver():
    beta, sigma = 2,-1
    atol, rtol = 1e-2, 1e-2
    # from analytical solution
    anal_period = 2* PI
    anal_radius = np.sqrt(beta)

    roots = cycles1(hopf_extended, init_hopf_ext, solve_ivp, args=(beta, sigma))
    numer_period = roots[-1]
    numer_radius = np.linalg.norm(roots[:-1])

    # check if period is a multiple of the analytical sol
    period_multiplicity = numer_period / anal_period
    period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
    print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
    print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
    return

def hopf_ext_mySolver():
        beta, sigma = 2,-1
        atol, rtol = 1e-2, 1e-2
        # from analytical solution
        anal_period = 2* PI
        anal_radius = np.sqrt(beta)

        roots = cycles1(hopf_extended, init_hopf_ext, args=(beta, sigma))
        numer_period = roots[-1]
        numer_radius = np.linalg.norm(roots[:-1])

        # check if period is a multiple of the analytical sol
        period_multiplicity = numer_period / anal_period
        period_multiple = np.isclose(period_multiplicity % 1, 1, atol=atol) or np.isclose(period_multiplicity % 1, 0, atol=atol)
        print(f'Analytical and numerical radius are numerically equivalent : {np.isclose(anal_radius, numer_radius, rtol=rtol)}')
        print(f'Numerical solution to radius is integer multiple of analytical solution : {period_multiple}')
        return

V1_times = []

start = time.time()
hopf_scipySolver()  # true
end  = time.time()
V1_times.append(end - start)

start = time.time()
hopf_mySolver()  # true
end  = time.time()
V1_times.append(end - start)

start = time.time()
hopf_ext_scipySolver()  # true
end  = time.time()
V1_times.append(end - start)

start = time.time()
hopf_ext_mySolver()  # true
end  = time.time()
V1_times.append(end - start)

print('hey')
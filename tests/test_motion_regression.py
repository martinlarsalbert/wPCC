import pytest
from src.models.regression import MotionRegression
import src.models.vmm_martin_simple as vmm
import numpy as np
import pandas as pd
from src.prime_system import PrimeSystem
import os
import dill
import pickle


@pytest.fixture
def data():

    N = 30
    columns = ["u1d", "v1d", "r1d", "u", "v", "r", "delta", "thrust"]
    d = np.random.normal(size=(N, len(columns)))  # random data
    df = pd.DataFrame(data=d, columns=columns)
    yield df


@pytest.fixture
def added_masses():
    added_masses_ = {
        "Xudot": 1.0,
        "Yvdot": 1.0,
        "Nrdot": 1.0,
        "Yrdot": 1.0,
        "Nvdot": 1.0,
    }
    yield added_masses_


@pytest.fixture
def ship_parameters():
    s = {
        "L": 1,
        "rho": 1,
        "I_z": 1,
        "m": 1,
        "x_G": 0,
        "X_rudder": -2.42219908951329,
    }
    yield s


@pytest.fixture
def prime_system(ship_parameters):
    ps = PrimeSystem(**ship_parameters)
    yield ps


def test_motion_regression(data, added_masses, prime_system, ship_parameters):

    regression = MotionRegression(
        vmm=vmm,
        data=data,
        added_masses=added_masses,
        prime_system=prime_system,
        ship_parameters=ship_parameters,
        exclude_parameters={"Xthrust": 1.0, "Ydelta": 1},
    )


def test_motion_regression_save(
    data, added_masses, prime_system, ship_parameters, tmpdir
):

    regression = MotionRegression(
        vmm=vmm,
        data=data,
        added_masses=added_masses,
        prime_system=prime_system,
        ship_parameters=ship_parameters,
        exclude_parameters={"Xthrust": 1.0},
    )
    file_path = os.path.join(str(tmpdir), "test.pkl")

    # for key, value in regression.__dict__.items():
    #    try:
    #        dill.dumps(value)
    #    except:
    #        a = 1

    regression.save(file_path=file_path)


def test_motion_regression_create_model(
    data, added_masses, prime_system, ship_parameters
):

    regression = MotionRegression(
        vmm=vmm,
        data=data,
        added_masses=added_masses,
        prime_system=prime_system,
        ship_parameters=ship_parameters,
        exclude_parameters={"Xthrust": 1.0},
    )

    model = regression.create_model(
        control_keys=["delta"],
    )

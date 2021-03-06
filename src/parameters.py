from src.symbols import *
import re
from src import prime_system


## Parameters
df_parameters = pd.DataFrame(columns=["symbol", "dof", "coord", "state", "denominator"])
dofs = ["X", "Y", "N"]
coords = ["u", "v", "r", r"\delta"]
states = ["", "dot"]


def get_parameter_denominator(dof, coord, state=""):

    numerator = prime_system.get_denominator(key=dof)  # X,Y,N...

    keys = []
    if state == "dot":
        key = f"{coord}1d"
        keys.append(key)
    else:
        keys = re.findall(r"[u v r]|delta|thrust|0", coord)

    assert len(keys) > 0

    denominator = prime_system.get_denominator(key=keys[0])
    for key in keys[1:]:
        denominator *= prime_system.get_denominator(key=key)

    parameter_denominator = numerator / denominator
    return parameter_denominator


def add_parameter(dof, coord, state=""):

    key = f"{dof}{coord}{state}"
    key = key.replace("\\", "")

    if len(state) > 0:
        symbol_name = r"%s_{\%s{%s}}" % (dof, state, coord)
    else:
        symbol_name = r"%s_{%s%s}" % (dof, state, coord)

    s = pd.Series(name=key, dtype="object")
    s["symbol"] = sp.symbols(symbol_name)
    s["dof"] = dof
    s["coord"] = coord
    s["state"] = state
    s["denominator"] = get_parameter_denominator(dof=dof, coord=coord, state=state)

    df_parameters.loc[key] = s


for dof in dofs:
    for coord in ["u", "v", "r"]:
        add_parameter(dof=dof, coord=coord, state="dot")

add_parameter(dof="X", coord="thrust")
add_parameter(dof="N", coord="thrust")
add_parameter(dof="Y", coord="thrust")
add_parameter(dof="X", coord="rrthrust")
add_parameter(dof="X", coord="0")
add_parameter(dof="Y", coord="0")
add_parameter(dof="Y", coord="0u")
add_parameter(dof="Y", coord="0uu")
add_parameter(dof="N", coord="0")
add_parameter(dof="N", coord="0u")
add_parameter(dof="N", coord="0uu")
add_parameter(dof="Y", coord="thrustdelta")
add_parameter(dof="N", coord="thrustdelta")
add_parameter(dof="X", coord="vvvv")


## Add all possible combinations:
from sklearn.preprocessing import PolynomialFeatures
import re

df_ = pd.DataFrame(
    columns=[
        "u",
        "v",
        "r",
        "delta",
    ],
    data=np.zeros((10, 4)),
)
polynomial_features = PolynomialFeatures(degree=3, include_bias=False)
polynomial_features.fit_transform(df_)
feature_names = polynomial_features.get_feature_names(df_.columns)


def rename(result):
    return result.group(1) * int(result.group(2))


feature_names = [
    re.sub(pattern=r"(\S+)\^(\d)", repl=rename, string=name) for name in feature_names
]
feature_names = [name.replace(" ", "") for name in feature_names]
for dof in dofs:
    for coord in feature_names:
        add_parameter(dof=dof, coord=coord)

## Parameters according to:
Xudot_ = m / (?? * sp.sqrt(L ** 3 / volume) - 14)  # [Brix] (SI)
Xudot_prime = Xudot_ / (1 / 2 * rho * L ** 3)
df_parameters.loc["Xudot", "brix"] = Xudot_prime  # [Brix]
df_parameters.loc["Yvdot", "brix"] = (
    -?? * (T / L) ** 2 * (1 + 0.16 * CB * B / T - 5.1 * (B / L) ** 2)
)  # [Clarke]
df_parameters.loc["Yrdot", "brix"] = (
    -?? * (T / L) ** 2 * (0.67 * B / L - 0.0033 * (B / T) ** 2)
)  # [Clarke]
df_parameters.loc["Nvdot", "brix"] = (
    -?? * (T / L) ** 2 * (1.1 * B / L - 0.04 * (B / T))
)  # [Clarke]
df_parameters.loc["Nrdot", "brix"] = (
    -?? * (T / L) ** 2 * (1 / 12 + 0.017 * CB * B / T - 0.33 * (B / L))
)  # [Clarke]
df_parameters.loc["Yv", "brix"] = -?? * (T / L) ** 2 * (1 + 0.4 * CB * B / T)  # [Clarke]
df_parameters.loc["Yr", "brix"] = (
    -?? * (T / L) ** 2 * (-1 / 2 + 2.2 * B / L - 0.08 * (B / T))
)  # [Clarke]
df_parameters.loc["Nv", "brix"] = -?? * (T / L) ** 2 * (1 / 2 + 2.4 * T / L)  # [Clarke]
df_parameters.loc["Nr", "brix"] = (
    -?? * (T / L) ** 2 * (1 / 4 + 0.039 * B / T - 0.56 * B / L)
)  # [Clarke]

mask = df_parameters["brix"].notnull()
df_parameters["brix_lambda"] = df_parameters.loc[mask, "brix"].apply(lambdify)

p = df_parameters["symbol"]

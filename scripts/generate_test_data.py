# this generates test data to make sure changes in the
# code do not destroy the values. If a new function is added
# this needs to be re run
#
#

import sys

import h5py

from astromodels.functions.function import _known_functions
from astromodels.functions.priors import *
from astromodels.utils.data_files import _get_data_file_path

eval_x = np.logspace(-1,3, 10)
_multiplicative_models = ["PhAbs", "TbAbs", "WAbs", "APEC", "VAPEC"]

input = int(sys.argv[-1])

file_path = _get_data_file_path("past_1D_values.h5")


if input == 0:
    # do not regenerate only add
    with h5py.File(file_path, "r") as f:

        already_known_functions = list(f.keys())

        flag = "a"

elif input == 1:

    already_known_functions = []

    flag = "w"

else:

    already_known_functions = None

print(input, already_known_functions)       




with h5py.File(file_path, flag) as f:
    if input == 1:

        f.create_dataset("eval_values", data=eval_x, compression="lzf")

    for key in _known_functions:

        if key in already_known_functions:

            continue

        this_function = _known_functions[key]

        # Test only the power law of XSpec, which is the only one we know we can test at 1 keV

        if key.find("XS")==0 and key != "XS_powerlaw" or (key in _multiplicative_models):

            # An XSpec model. Test it only if it's a power law (the others might need other parameters during
            # initialization)

            continue

        if key.find("TemplateModel")==0:

            # The TemplateModel function has its own test

            continue

    #            continue

        if this_function._n_dim == 1:

            print(f"testing {key} ...")

            func = this_function()

            data=func(eval_x)

            print(data)

            f.create_dataset(key, data=np.atleast_1d(data), compression="lzf")



from data.CPUS_data import CPUS
from data.MOTHERBOARDS_data import MOTHERBOARDS
from data.RAMS_data import RAMS
from data.GPUS_data import GPUS
from data.PSUS_data import PSUS
from data.CASES_data import CASES


COMPONENTS = {
    "CPU": CPUS,
    "MOTHERBOARD": MOTHERBOARDS,
    "RAM": RAMS,
    "GPU": GPUS,
    "PU" : PSUS,
    "CASE": CASES
}
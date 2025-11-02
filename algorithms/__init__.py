from .CP import run_CP
from .Cliquer import run_Cliquer
from .MCQ import MCQ
from .MCR import MCR
from .DK import run_DK
from .DF import run_DF
from .χ import run_χ
from .χ_DF import run_χ_DF

ALGORITHMS = {
    'CP': run_CP,
    'Cliquer': run_Cliquer,
    'MCQ': MCQ,
    'MCR': MCR,
    'DK': run_DK,
    'DF': run_DF,
    'χ': run_χ,
    'χ+DF': run_χ_DF,
}

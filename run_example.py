from run import *
from types import SimpleNamespace

from autoarchaeologist.base import excavation

from autoarchaeologist.generic.bigdigits import BigDigits
from autoarchaeologist.generic.samesame import SameSame
from autoarchaeologist.data_general.absbin import AbsBin
from autoarchaeologist.data_general.papertapechecksum import DGC_PaperTapeCheckSum

class ExampleExcavation(excavation.Excavation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_examiner(BigDigits)
        self.add_examiner(AbsBin)
        self.add_examiner(DGC_PaperTapeCheckSum)
        self.add_examiner(SameSame)

if __name__ == "__main__":
    example_arguments = SimpleNamespace()
    example_arguments.dir = "."
    example_arguments.filename = "examples/30001393.bin"
    args = process_arguments(example_arguments)

    try:
        os.mkdir(args.dir)
    except FileExistsError:
        pass

    perform_excavation(args, ("excavator", ExampleExcavation))

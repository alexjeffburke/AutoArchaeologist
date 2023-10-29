'''
(C)CP/M Artifacts from Datamuseum.dk's BitStore
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

'''

from autoarchaeologist import ddhf

from autoarchaeologist.base import type_case

from autoarchaeologist.generic import samesame
from autoarchaeologist.generic import textfiles
from autoarchaeologist.DigitalResearch import cpm

class TxtFile(textfiles.TextFile):
    VERBOSE=False
    MAX_TAIL=2048

cpm.cpm_filename_typecase.set_slug(0x5f, '_', '_')
cpm.cpm_filename_typecase.set_slug(0x3b, ';', ';')

class Cpm_Ds2089(type_case.DS2089):
    ''' ... '''

    def __init__(self):
        super().__init__()
        self.set_slug(0x0d, ' ', '')
        self.set_slug(0x1a, ' ', '«eof»', self.EOF)

        self.set_slug(0x00, ' ', '«nul»')
        #self.set_slug(0x07, ' ', '«bel»')
        #self.set_slug(0x0c, ' ', '«ff»\n')
        #self.set_slug(0x0e, ' ', '«so»')
        #self.set_slug(0x0f, ' ', '«si»')
        #self.set_slug(0x19, ' ', '«eof»', self.EOF)
        #self.set_slug(0x7f, ' ', '')

class CpmTypeCase(type_case.Ascii):

    def __init__(self):
        super().__init__()
        self.set_slug(0x0d, ' ', '')
        self.set_slug(0x1a, ' ', '«eof»', self.EOF)

class Cpm(ddhf.DDHF_Excavation):

    ''' All Cpm artifacts '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.type_case = Cpm_Ds2089()

        self.add_examiner(cpm.CpmFileSystem)
        self.add_examiner(TxtFile)
        self.add_examiner(samesame.SameSame)

        if False:
            self.from_bitstore(
                "30004681",
            )
            return

        self.from_bitstore(
            "-30002875", # PASCAL
            "-30003268", # Ligner CP/M men med COMAL-80 navne semantik
            "-30003296", # Ikke CP/M format
            "RC/RC700",
            "RC/RC750",
            "RC/RC759",
            "RC/RC850/CPM",
            "RC/RC890",
            "CR/CR7",
            "CR/CR8",
            "CR/CR16",
            "JET80",
            "COMPANY/ICL/COMET",
            "COMPANY/BOGIKA",
            media_types = (
                '5¼" Floppy Disk',
                '8" Floppy Disk',
            )
        )

if __name__ == "__main__":
    ddhf.main(
        Cpm,
        html_subdir="cpm",
        ddhf_topic = 'CP/M',
        ddhf_topic_link = 'https://datamuseum.dk/wiki'
    )
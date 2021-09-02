'''
   TAR(1) format
'''

import html
import time

from autoarchaeologist.unix.unix_file_mode import unix_file_mode

class Invalid(Exception):
    ''' invalid tar file '''

class TarEntry():
    ''' One tar(1) file entry '''

    def __init__(self, that, offset):
        self.hdr = that[offset:offset+512].tobytes()
        self.parse_header()
        self.filename = that.type_case.decode(self.filename)
        if self.target:
            self.target = that.type_case.decode(self.target)
        if self.link == 0 and self.size:
            self.this = that.create(start=offset + 512, stop=offset + 512 + self.size)
            self.this.set_name(self.filename)
            self.this.by_class[TarFile] = self
        else:
            self.this = None
        self.next = offset + 512 * (1 + (self.size + 511) // 512)

    def parse_header(self):
        ''' Parse the tar header '''
        self.csum = self.oct(148, 8)
        if self.csum != sum(self.hdr[:148]) + sum(self.hdr[156:]) + 8 * 32:
            raise Invalid("Checsum does not match")
        self.filename = self.hdr[:100].split(b'\x00')[0]
        self.link = self.oct(156, 1)
        self.mode = 0
        self.uid = 0
        self.gid = 0
        self.size = 0
        self.mtime = 0
        try:
            self.mode = self.oct(100, 8)
            self.uid = self.oct(108, 8)
            self.gid = self.oct(116, 8)
            self.size = self.oct(124, 12)
            self.mtime = self.oct(136, 12)
        except Invalid:
            if not self.link:
                raise
        if self.link:
            self.target = self.hdr[157:257].split(b'\x00')[0]
        else:
            self.target = None

    def oct(self, offset, width):
        ''' Return numeric value of octal field '''
        try:
            retval = self.hdr[offset:offset + width]
            retval = retval.split(b'\x00')[0]
            retval = retval.decode('ascii')
            if len(retval) == 0:
                return 0
            retval = int(retval, 8)
            return retval
        except:
            raise Invalid(
                "Bad octal field [%d:%d] %s" % (
                    offset,
                    offset + width,
                    str(self.hdr[offset:offset + width]
                    )
                )
            )

    def render(self, fo):
        ''' as tar -tvf would '''
        fo.write(unix_file_mode(self.mode))
        fo.write(" %d %5d %5d %8d " % (self.link, self.uid, self.gid, self.size))
        fo.write(time.ctime(self.mtime) + " ")
        if self.this:
            fo.write(self.this.summary())
        else:
            fo.write(html.escape(self.filename))
        if self.link == 1:
            fo.write(" link to " + html.escape(self.target))
        fo.write("\n")

class TarFile():

    ''' A UNIX tar(1) file '''

    def __init__(self, this):
        if len(this) <= 512:
            return
        try:
            entry = TarEntry(this, 0)
        except Invalid as e:
            # print("TAR", this, e)
            return
        if TarFile in this.parents[0].by_class:
            return
        self.children = [entry]
        this.type = "Tar_file"
        this.add_note("Tar_file")
        this.by_class[TarFile] = self
        while entry.next < len(this) and this[entry.next]:
            entry = TarEntry(this, entry.next)
            self.children.append(entry)
        this.add_interpretation(self, self.render)

    def render(self, fo, _this):
        ''' ... '''
        fo.write("<H3>Tar(1) file</H3>\n")
        fo.write("<pre>\n")
        for i in self.children:
            i.render(fo)
        fo.write("</pre>\n")
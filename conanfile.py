from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from shutil import copyfile
import os

class Libmpeg2Conan(ConanFile):
    name = "libmpeg2"
    version = "0.5.1"
    description = "libmpeg2 is a free library for decoding mpeg-2 and mpeg-1 video streams"
    url = "https://github.com/conanos/libmpeg2"
    homepage = "http://libmpeg2.sourceforge.net/"
    license = "GPLv2Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        #http://libmpeg2.sourceforge.net/files/libmpeg2-0.5.1.tar.gz

        tools.get('http://172.16.64.65:8081/artifactory/gstreamer/{name}-{version}.tar.gz'.format(name=self.name, version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            self.run('autoreconf -f -i')

            _args = ["--prefix=%s/builddir"%(os.getcwd()), "--disable-silent-rules", "--enable-introspection"]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

        #self.run('autoreconf -f -i')
        #copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/.auto/config.guess"%(os.getcwd()))
        #copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/.auto/config.sub"%(os.getcwd()))
        #self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
        #' --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
        #self.run('make -j4')
        #self.run('make install')

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)


# Misc
from pathlib import Path

# Conan Tools
from conan import ConanFile
from conan.tools.build import cross_building
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools.scm import Git

required_conan_version = ">=1.54.0"


class BasicConanfile(ConanFile):
    name = "conantemplate"
    version = "1.0"
    description = "A Conan Template"
    license = "NA"
    homepage = "NA"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "coverage": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "coverage": False,
    }

    package_type = "application"
    no_copy_source = True

    exports_sources = ("CMakeLists.txt", "src/*", "include/*")

    def source(self):
        git = Git(self)
        git.clone(
            url="https://github.com/aasalim/HelloWorld.git",
            target="external/HelloWorld",
        )
        self.run("cd external/HelloWorld && make conancreate")

    def build_requirements(self):
        self.requires("gtest/1.12.1")
        self.requires("spdlog/1.13.0")
        self.requires("systemc/2.3.4")

    def requirements(self):
        self.requires("helloworld/1.0")

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        self.folders.build = "build"
        self.folders.package = "package"
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self, generator="Ninja")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        install_path = Path(self.build_folder) / self.folders.package
        cmake.configure(
            variables={
                "CMAKE_INSTALL_PREFIX": install_path,
                "COVERAGE": self.options.coverage,
                "CONAN_PACKAGE_VERSION": self.version,
            }
        )
        cmake.build()
        cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.srcdirs = ["src"]
        self.cpp_info.libs = ["helloworld"]
        self.cpp_info.includedirs = ["include"]

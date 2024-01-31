cmake_minimum_required(VERSION 3.22)
project(ConanTemplate)

enable_testing()
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Options: Things you can set via commandline options to cmake (e.g. -DENABLE_LTO=[ON|OFF])
option(ENABLE_WARNINGS_SETTINGS "Allow target_set_warnings to add flags and defines.
                                 Set this to OFF if you want to provide your own warning parameters." ON)

option(ENABLE_LTO "Enable link time optimization" ON)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
include(LTO)
include(Warnings)
include(GoogleTest)
include(Cache)

# Check for LTO support.
find_lto(CXX)

# Enable Cache
check_enable_cache()

option(COVERAGE "Generate coverage data" ON)

if(COVERAGE)
    include(CodeCoverage)
    append_coverage_compiler_flags()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O0")

    # Enable Static Analysis
    include(StaticAnalyzers)
    tool_enable_cppcheck(ON "")
endif()

message(STATUS "COVERAGE = ${COVERAGE}")

add_subdirectory(src)

if(NOT CMAKE_CROSSCOMPILING)
    find_package(spdlog REQUIRED)
    find_package(GTest REQUIRED)
    find_package(SystemCLanguage REQUIRED)
    add_subdirectory(tests)
endif()

install(TARGETS ConanTemplate)

file(GLOB PUBLIC_HEADERS
    ${CMAKE_CURRENT_SOURCE_DIR}/include/*.h
)

install(FILES ${PUBLIC_HEADERS} DESTINATION include)
install(FILES LICENSE DESTINATION licenses)
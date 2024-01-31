
add_executable(UnitTests UT_Test1.cpp)

target_link_libraries(UnitTests
    PUBLIC
    GTest::gtest_main
    GTest::gmock
    spdlog::spdlog
)

target_set_warnings(UnitTests ENABLE ALL AS_ERROR ALL DISABLE Annoying)
gtest_discover_tests(UnitTests)

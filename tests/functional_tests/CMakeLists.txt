# Integration Tests
add_executable(FuntionalTest1 funtional_test1.cpp)
target_link_libraries(FuntionalTest1 fmt::fmt SystemC::systemc)
add_test(NAME FuntionalTest1 COMMAND FuntionalTest1)
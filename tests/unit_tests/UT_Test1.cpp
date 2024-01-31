#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include <spdlog/spdlog.h>

class UnitTest : public ::testing::Test {
protected:
    // Setup code that will be called before each test
    void SetUp() override
    {
        spdlog::default_logger_raw()->set_level(spdlog::level::debug);
        // Initialize resources, if needed
    }

    // Teardown code that will be called after each test
    void TearDown() override
    {
        // Clean up resources, if needed
    }
};

TEST_F(UnitTest, UnitTest1)
{
    /* Arrange */

    /* Act */

    /* Assert */
    EXPECT_EQ(0, false);
}

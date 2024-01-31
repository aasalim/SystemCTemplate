#include <fmt/color.h>
#include <fmt/core.h>
#include <systemc>
using namespace sc_core;

#define EXPECT_EQ(a, b)                                                                            \
    if (a != b) {                                                                                  \
        throw std::runtime_error(fmt::format(fg(fmt::rgb(0xFF0000)),                               \
            "\nExpected {}({}) to equal {}({})\nIn file: {}:{}", #a, a, #b, b, __FILE__,           \
            __LINE__));                                                                            \
    }

SC_MODULE(Processor)
{
    sc_port<sc_signal<int>> Time;

    SC_CTOR(Processor) { SC_THREAD(test); }
    void test()
    {
        uint8_t i = 0;
        while (true) {
            int tick = sc_time_stamp().to_seconds();
            Time->write(tick);
            EXPECT_EQ(i, tick);

            i++;
            wait(1, SC_SEC);
        }
    }
};
int sc_main(int, char*[])
{
    sc_trace_file* file = sc_create_vcd_trace_file("test1");

    Processor proc("Processor");

    sc_signal<int> Time;

    proc.Time(Time);

    sc_trace(file, Time, "Time");

    sc_start(3, SC_SEC);

    sc_close_vcd_trace_file(file);

    return 0;
}
// C++ echo binary for the dimos-lcm benchmark harness.
//
// Usage: echo <lcm_type> <input_channel> <output_channel>
//
// Subscribes to <input_channel>, decodes incoming messages as the
// requested LCM type via a compile-time dispatch table, re-encodes,
// and republishes on <output_channel>. Prints "READY\n" once the
// subscription is in place so the harness can begin measuring.
//
// The dispatch table only knows the menu types defined by the
// benchmark — adding a new type means adding an entry below AND
// regenerating C++ bindings if the type is new to the repo.

#include <atomic>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <string>
#include <unordered_map>

#include <lcm/lcm-cpp.hpp>

#include "std_msgs/Int32.hpp"
#include "geometry_msgs/PoseStamped.hpp"
#include "sensor_msgs/Imu.hpp"
#include "tf2_msgs/TFMessage.hpp"
#include "sensor_msgs/LaserScan.hpp"
#include "sensor_msgs/Image.hpp"
#include "sensor_msgs/PointCloud2.hpp"

namespace {

std::atomic<bool> g_stop{false};

void handle_signal(int /*signo*/) { g_stop.store(true); }

// One templated handler per benchmark menu type. The `lcm::ReceiveBuffer`
// gives us the raw bytes; we decode into the typed message, then encode
// back out. We deliberately go through the typed struct so this measures
// the real codec work rather than a memcpy.
template <typename Msg>
class TypedEchoHandler {
 public:
    TypedEchoHandler(lcm::LCM* lc, std::string out_channel)
        : lc_(lc), out_channel_(std::move(out_channel)) {}

    void on_message(const lcm::ReceiveBuffer* rbuf,
                    const std::string& /*channel*/) {
        Msg msg;
        if (msg.decode(rbuf->data, 0, rbuf->data_size) < 0) {
            std::fprintf(stderr, "echo: decode failed\n");
            return;
        }
        lc_->publish(out_channel_, &msg);
    }

 private:
    lcm::LCM* lc_;
    std::string out_channel_;
};

// Each entry registers a subscription on the lcm handle and keeps the
// handler alive for the program's lifetime.
struct Registrar {
    using Fn = std::function<void(lcm::LCM*, const std::string&,
                                   const std::string&)>;
    Fn install;
};

template <typename Msg>
Registrar make_registrar() {
    return Registrar{[](lcm::LCM* lc, const std::string& in,
                        const std::string& out) {
        // Leak the handler intentionally — its lifetime is the program.
        auto* handler = new TypedEchoHandler<Msg>(lc, out);
        auto* sub = lc->subscribe(
            in, &TypedEchoHandler<Msg>::on_message, handler);
        // LCM's default queue capacity is 30; the throughput profile
        // bursts hundreds of messages before draining, so anything
        // smaller silently drops at the receiver and skews results.
        sub->setQueueCapacity(4096);
    }};
}

const std::unordered_map<std::string, Registrar>& dispatch_table() {
    static const std::unordered_map<std::string, Registrar> table = {
        {"std_msgs_Int32",            make_registrar<std_msgs::Int32>()},
        {"geometry_msgs_PoseStamped", make_registrar<geometry_msgs::PoseStamped>()},
        {"sensor_msgs_Imu",           make_registrar<sensor_msgs::Imu>()},
        {"tf2_msgs_TFMessage",        make_registrar<tf2_msgs::TFMessage>()},
        {"sensor_msgs_LaserScan",     make_registrar<sensor_msgs::LaserScan>()},
        {"sensor_msgs_Image",         make_registrar<sensor_msgs::Image>()},
        {"sensor_msgs_PointCloud2",   make_registrar<sensor_msgs::PointCloud2>()},
    };
    return table;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 4) {
        std::fprintf(stderr,
                     "usage: echo <lcm_type> <input_channel> <output_channel>\n");
        return 64;
    }
    const std::string type_name = argv[1];
    const std::string in_channel = argv[2];
    const std::string out_channel = argv[3];

    const auto& table = dispatch_table();
    auto it = table.find(type_name);
    if (it == table.end()) {
        std::fprintf(stderr, "echo: unknown lcm type %s\n", type_name.c_str());
        return 2;
    }

    lcm::LCM lc("udpm://239.255.76.67:7667?ttl=0");
    if (!lc.good()) {
        std::fprintf(stderr, "echo: failed to initialize LCM\n");
        return 1;
    }

    it->second.install(&lc, in_channel, out_channel);

    std::signal(SIGTERM, handle_signal);
    std::signal(SIGINT, handle_signal);

    std::printf("READY\n");
    std::fflush(stdout);

    while (!g_stop.load()) {
        // 100ms poll keeps shutdown latency low without burning CPU.
        lc.handleTimeout(100);
    }
    return 0;
}

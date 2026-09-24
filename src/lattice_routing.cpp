#include <iostream>
#include <vector>
#include <array>
#include <cstdint>
#include <cmath>
#include "structural_locks.h"
#include "routing_rules.h"

// Represents a data packet moving through the structural lattice
struct DataPacket {
    uint64_t packet_id;
    std::array<int, 14> coordinate;
    std::array<int, 3> velocity_vector;
    uint32_t payload_size;
    StreamPriority priority;
};

class LatticeRoutingEngine {
private:
    const double routing_eta = MANIFOLD_ETA;
    const double density_floor = MATRIX_DENSITY_LIMIT;

    uint16_t calculate_node_phase(uint64_t node_i, int position_x) {
        uint64_t raw_step = (node_i * 89) + (static_cast<uint64_t>(std::abs(position_x)) * 27);
        return static_cast<uint16_t>(raw_step % 144);
    }

public:
    LatticeRoutingEngine() {}

    // Process packet transmission through the deterministic coordinate manifold
    bool route_packet(DataPacket& packet) {
        // Create local workspace structures to hold state before committing the step
        std::array<int, 14> temp_coordinate = packet.coordinate;
        std::array<int, 3> temp_velocity = packet.velocity_vector;

        for (int dim = 0; dim < 3; ++dim) {

            // 1. Rule 2 Implementation: Verify boundaries using the temporary tracker
            if (PathfindingRules::check_boundary_breach(temp_coordinate[dim], temp_velocity[dim])) {
                packet.velocity_vector[dim] = -packet.velocity_vector[dim];
                return false; // Reject entire step state; update velocity direction
            }

            int next_step = temp_coordinate[dim] + temp_velocity[dim];

            // 2. Rule 3 Implementation: Audit phase density boundaries
            uint16_t local_phase = calculate_node_phase(packet.packet_id, next_step);
            RoutingAction density_action = PathfindingRules::evaluate_matrix_density(local_phase);

            if (density_action == RoutingAction::PHASE_SHIFT) {
                packet.velocity_vector[dim] = -packet.velocity_vector[dim];
                return false; // Reject step state; shift direction profile
            }

            // Write to local temporary array state only
            temp_coordinate[dim] = next_step;
        }

        // Commit step changes to the global data struct ONLY if all 3 dimensions cleared
        packet.coordinate = temp_coordinate;
        return true;
    }
};

int main() {
    LatticeRoutingEngine engine;

    DataPacket test_packet = {
        102489,
        {{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1}},
        {{1, -1, 1}},
        256,
        StreamPriority::LIGHT_STREAM
    };

    std::cout << "[E] Register: Initializing core network routing logic execution test..." << std::endl;

    int successful_steps = 0;
    for (int step = 0; step < 1000; ++step) {
        if (engine.route_packet(test_packet)) {
            successful_steps++;
        }
    }

    std::cout << "Test loop complete. Clear advances: " << successful_steps << "/1000 steps." << std::endl;
    std::cout << "Updated packet coordinates: ["
    << test_packet.coordinate[0] << ", "
    << test_packet.coordinate[1] << ", "
    << test_packet.coordinate[2] << "]" << std::endl;

    return 0;
}

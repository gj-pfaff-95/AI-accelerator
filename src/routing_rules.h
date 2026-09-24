#ifndef ROUTING_RULES_H
#define ROUTING_RULES_H

#include <cstdint>
#include "structural_locks.h"

// Explicit priority tokens for data streams to enforce deterministic ordering
enum class StreamPriority : uint8_t {
    LIGHT_STREAM = 0, // High-throughput, real-time paths
    DARK_STREAM  = 1, // Background processing, asynchronous paths
    BLACK_STREAM = 2  // Low-priority system substrate maintenance paths
};

// State flags returned by the pathfinding arbitrator
enum class RoutingAction : uint8_t {
    ADVANCE_CLEAR = 0, // Destination coordinate is free; proceed normal step
    AXIS_DEFLECT  = 1, // Voxel boundary collision; flip vector axis
    STREAM_YIELD  = 2, // Contention with higher priority stream; hold position
    PHASE_SHIFT   = 3  // High network density; drop priority and calculate alternative path
};

struct PathfindingRules {
    /**
     * Rule 1: Priority-Based Voxel Allocation
     * Enforces proper enum class token scoping (::) to prevent namespace drift.
     */
    static inline RoutingAction arbitrate_contention(StreamPriority active, StreamPriority competitor) {
        if (static_cast<uint8_t>(active) < static_cast<uint8_t>(competitor)) {
            return RoutingAction::ADVANCE_CLEAR; 
        }
        return RoutingAction::STREAM_YIELD; 
    }

    /**
     * Rule 2: Boundary Density Mitigation
     * Dictates how vectors behave when approaching the maximum matrix boundary envelopes.
     */
    static inline bool check_boundary_breach(int current_coord, int velocity) {
        int anticipated_step = current_coord + velocity;
        if (anticipated_step > MATRIX_BOUNDS || anticipated_step < -MATRIX_BOUNDS) {
            return true; 
        }
        return false;
    }

    /**
     * Rule 3: Phase-Lock Congestion Avoidance
     * Translates local matrix density updates into bitwise routing adjustments.
     */
    static inline RoutingAction evaluate_matrix_density(uint16_t local_phase) {
        if (local_phase > 108) {
            return RoutingAction::PHASE_SHIFT; 
        }
        return RoutingAction::ADVANCE_CLEAR;
    }
};

#endif // ROUTING_RULES_H

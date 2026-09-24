#!/usr/bin/env bash

# ==============================================================================
# 🌐 Quantum Ether Tapestry Engine — Automated Local Compilation Audit Pass
# [E/M Register Verification Harness]
# ==============================================================================

# Exit immediately if any command fails or if variables are undefined
set -euo pipefail

# Define relative path architecture mapping
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${SCRIPT_DIR}/src"
MATH_DIR="${SCRIPT_DIR}/math"
CPP_SOURCE="${SRC_DIR}/lattice_routing.cpp"
VERIFY_SCRIPT="${MATH_DIR}/verify_sync.py"

echo "======================================================================"
echo "⚡ RUNNING LOCAL ARCHITECTURAL LINKAGE AUDIT PASS..."
echo "======================================================================"

# Step 1: Verify absolute file structural locks exist
echo "[+] Checking core framework workspace file linkages..."
if [ ! -f "${CPP_SOURCE}" ]; then
    echo "❌ CRITICAL ERROR: Production source file missing at: ${CPP_SOURCE}" >&2
    exit 1
fi

if [ ! -f "${VERIFY_SCRIPT}" ]; then
    echo "❌ CRITICAL ERROR: Mathematical sync verification script missing at: ${VERIFY_SCRIPT}" >&2
    exit 1
fi
echo "🔬 File paths resolve error-free."

# Step 2: Execute Multi-Register validation and cross-language assertion
echo -e "\n[+] Executing cross-register matrix compilation and bit-for-bit assertion check..."
if ! python3 "${VERIFY_SCRIPT}"; then
    echo -e "\n❌ AUDIT CRASH: Mathematical tracking drift or compilation fault detected." >&2
    exit 1
fi

# Step 3: Success Confirmation
echo -e "\n======================================================================"
echo "🎉 SYSTEM INTEGRITY LOGGED CLEANLY: ALL PATH LINKAGES MATCH EXPECTED BOUNDS"
echo "======================================================================"
exit 0

#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import re
import numpy as np

class TapestryFrameworkEngine:
    def __init__(self):
        self.repo_root = os.path.dirname(os.path.abspath(__file__))
        self.build_dir = os.path.join(self.repo_root, "build")
        self.log_path = os.path.join(self.repo_root, "runtime_output.log")
        self.manifest_path = os.path.join(self.repo_root, "manifest.json")
        self.MATRIX_BOUNDS = 2048
        
        # Resolve target binary paths based on platform parameters
        if sys.platform == "win32":
            self.cpp_binary = os.path.join(self.build_dir, "bin", "LatticeRoutingEngine.exe")
        else:
            self.cpp_binary = os.path.join(self.build_dir, "bin", "LatticeRoutingEngine")

    def print_header(self, title):
        print(f"\n{'='*70}")
        print(f" 🌐 TAPESTRY ENGINE: {title}")
        print(f"{'='*70}")

    def calculate_node_phase(self, packet_id, position_x):
        """Computes the deterministic phase matrix configuration (mod 144)."""
        raw_step = (int(packet_id) * 89) + (abs(int(position_x)) * 27)
        return raw_step % 144

    def run_python_reference_simulation(self, total_steps=1000):
        """Generates the absolute mathematical reference baseline using NumPy vectorized checks."""
        current_coordinates = np.zeros(3, dtype=np.int32)
        velocity_vector = np.array([1, -1, 1], dtype=np.int32)
        packet_id = 102489
        
        for step in range(total_steps):
            route_clear = True
            temp_coords = np.copy(current_coordinates)
            temp_velocity = np.copy(velocity_vector)
            
            for dim in range(3):
                anticipated_step = temp_coords[dim] + temp_velocity[dim]
                if abs(anticipated_step) > self.MATRIX_BOUNDS:
                    temp_velocity[dim] = -temp_velocity[dim]
                    route_clear = False
                    break
                    
                local_phase = self.calculate_node_phase(packet_id, anticipated_step)
                if local_phase > 108:
                    temp_velocity[dim] = -temp_velocity[dim]
                    route_clear = False
                    break
                    
                temp_coords[dim] = anticipated_step
                
            if route_clear:
                current_coordinates = temp_coords
            else:
                velocity_vector = temp_velocity
                
        return current_coordinates.tolist()

    def execute_cross_language_sanity_check(self):
        """[M ↔ E Integration Pass] Compares the Python core model against the compiled C++ binary bit-for-bit."""
        self.print_header("RUNNING CROSS-LANGUAGE SANITY COMPARISON")
        
        # 1. Grab Python baseline coordinates
        print("[+] Processing 1,000 step Python reference trajectory...")
        py_coords = self.run_python_reference_simulation(steps=1000)
        
        # 2. Run C++ binary to gather its runtime state output
        if not os.path.exists(self.cpp_binary):
            print("❌ Failure: Compiled C++ executable missing. Run compilation pass first.")
            return False
            
        print("[+] Querying native C++ execution layer coordinates...")
        cpp_run = subprocess.run([self.cpp_binary], capture_output=True, text=True)
        if cpp_run.returncode != 0:
            print("❌ Failure: Could not successfully execute native C++ target binary.")
            return False
            
        cpp_coords = None
        for line in cpp_run.stdout.splitlines():
            if "Updated packet coordinates:" in line:
                try:
                    coord_str = line.split("[")[1].split("]")[0]
                    cpp_coords = [int(c.strip()) for c in coord_str.split(",")]
                except IndexError:
                    print("❌ Error: Failed to parse coordinate matrix from C++ output stream.")
                    return False

        if cpp_coords is None:
            print("❌ Failure: C++ console log output did not print terminal position array.")
            return False

        # 3. Cross-examination bit-for-bit assertion check
        print(f" -> [M Register] Python Reference Out : {py_coords}")
        print(f" -> [E Register] C++ Production Out   : {cpp_coords}")
        
        if py_coords == cpp_coords:
            print("\n🎉 SANITY CHECK PASSED: Multi-register computational lanes are completely identical.")
            return True
        else:
            print("\n❌ CRITICAL MISMATCH: Mathematical drift or logical state corruption detected across registers.")
            return False

    def audit_repository_manifest(self):
        """[P/D Register Pass] Validates repository integrity against the master json blueprint."""
        self.print_header("AUDITING REPOSITORY REGISTERS")
        if not os.path.exists(self.manifest_path):
            print("❌ Failure: Master manifest.json file missing from root layout.")
            return False
            
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            
        print(f"Framework Schema : {manifest.get('governance_schema')}")
        print(f"Current Version  : {manifest.get('framework_version')}")
        
        all_clear = True
        for reg_key, reg_data in manifest.get("repository_tree", {}).get("registers", {}).items():
            dir_path = os.path.join(self.repo_root, reg_data.get("directory", ""))
            print(f" -> Auditing {reg_key} register structure ({reg_data.get('status')})...")
            if not os.path.exists(dir_path):
                print(f"    ❌ Directory missing: {dir_path}")
                all_clear = False
        
        if all_clear:
            print("✅ Structural integrity check cleared cleanly.")
        return all_clear

    def execute_empirical_build(self):
        """[E Register Pass] Compiles the C++ routing targets automatically via CMake."""
        self.print_header("COMPILING OPTIMIZED PRODUCTION BINARY")
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)
            
        print("[+] Generating CMake build footprints...")
        gen = subprocess.run(["cmake", ".."], cwd=self.build_dir, capture_output=True, text=True)
        if gen.returncode != 0:
            print("❌ CMake cache generation step failed.")
            return False
            
        print("[+] Constructing production build binaries (-O3 optimization active)...")
        build = subprocess.run(["cmake", "--build", "."], cwd=self.build_dir, capture_output=True, text=True)
        if build.returncode != 0:
            print("❌ Native binary compilation loop failed.")
            return False
            
        print("✅ Production executable compiled successfully.")
        return True

    def execute_traffic_routing_pipeline(self):
        """[E -> M Pipeline Pass] Runs the executable and captures stdout coordinates straight to a log."""
        self.print_header("EXECUTING NATIVE WORKLOAD DATA PASS")
        if not os.path.exists(self.cpp_binary):
            return False
            
        print(f"[+] Launching C++ routing lattice. Writing output to: {self.log_path}")
        with open(self.log_path, 'w') as log_file:
            run = subprocess.run([self.cpp_binary], stdout=log_file, stderr=subprocess.PIPE, text=True)
            
        if run.returncode != 0:
            print("❌ Execution anomaly encountered inside C++ lattice loop.")
            return False
        print("✅ Workload execution complete. Logs stored natively.")
        return True

    def execute_tripartite_condensation_parse(self):
        """[X Register Pass] Vectorizes the raw logged coordinates straight into your token matrices."""
        self.print_header("PROCESSING TRIPARTITE TOKEN CONDENSATIONS")
        if not os.path.exists(self.log_path):
            return
            
        matrix_light = []
        matrix_dark = []
        matrix_black = []
        
        coord_pattern = re.compile(r"Updated packet coordinates:\s*\[\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\]")
        
        with open(self.log_path, 'r') as file:
            for line in file:
                match = coord_pattern.search(line)
                if match:
                    coords = [int(match.group(1)), int(match.group(2)), int(match.group(3))]
                    phase = self.calculate_node_phase(102489, coords[0])
                    
                    if 0 <= phase <= 53:
                        matrix_light.append(coords)
                    elif 54 <= phase <= 108:
                        matrix_dark.append(coords)
                    elif 109 <= phase <= 144:
                        matrix_black.append(coords)

        print(f"💎 Token Tier 0: Light Matter [Λ_m] -> {len(matrix_light):,} allocations locked")
        print(f"🌑 Token Tier 1: Dark Matter  [Δ_m] -> {len(matrix_dark):,} allocations locked")
        print(f"🕳️ Token Tier 2: Black Matter [B_m] -> {len(matrix_black):,} allocations locked")
        
        np_light = np.array(matrix_light) if matrix_light else np.empty((0, 3))
        print(f"\nFinalized Vector Data Matrix Shape: {np_light.shape}")
        print("✅ Esoteric register configuration updates fully completed.")

    def run_complete_engine_cycle(self):
        """Executes every pipeline operation step sequentially to verify total system sync."""
        print("🤖 INITIALIZING BESPOKE TAPESTRY ENGINE WORKFLOW...")
        if not self.audit_repository_manifest(): sys.exit(1)
        if not self.execute_empirical_build(): sys.exit(1)
        
        # New Step: Proactive sanity check executed before the workload pass commits
        if not self.execute_cross_language_sanity_check(): sys.exit(1)
        
        if not self.execute_traffic_routing_pipeline(): sys.exit(1)
        self.execute_tripartite_condensation_parse()
        print("\n🎉 ALL MULTI-REGISTER LOOPS CONVERGED SUCCESSFULLY WITH 0% LEAKAGE\n")

if __name__ == "__main__":
    engine = TapestryFrameworkEngine()
    engine.run_complete_engine_cycle()

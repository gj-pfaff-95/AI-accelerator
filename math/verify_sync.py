import subprocess
import sys
import os
from route_validator import LatticeRouteValidator

class CrossLanguageVerifier:
    def __init__(self, cpp_source_path, cpp_binary_path):
        self.cpp_source = cpp_source_path
        self.cpp_binary = cpp_binary_path
        self.validator = LatticeRouteValidator()

    def compile_cpp_engine(self):
        """Compiles the C++ routing logic using standard g++ optimization flags."""
        print(f"[M] Register: Compiling {self.cpp_source}...")
        if not os.path.exists(self.cpp_source):
            print(f"❌ Error: Source file not found at {self.cpp_source}")
            return False
            
        compile_cmd = ["g++", "-O3", self.cpp_source, "-o", self.cpp_binary]
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Compilation failed:")
            print(result.stderr)
            return False
        print("✅ C++ compilation successful.")
        return True

    def run_cpp_engine(self, steps):
        """Executes the compiled C++ binary and extracts its final state coordinates."""
        # Note: In a production test, pass the step count directly via a CLI argument or config
        print(f"[M] Register: Running C++ execution layer for {steps:,} steps...")
        result = subprocess.run([self.cpp_binary], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ C++ Execution Error:")
            print(result.stderr)
            return None
            
        # Parse the coordinates from stdout output text
        # Assumes format: "Updated packet coordinates: [X, Y, Z]"
        for line in result.stdout.splitlines():
            if "Updated packet coordinates:" in line:
                coord_str = line.split("[")[1].split("]")[0]
                return [int(c.strip()) for c in coord_str.split(",")]
        return None

    def execute_cross_audit(self, steps=1000):
        """Compares the Python mathematical model outputs directly against the C++ binary results."""
        print("==================================================")
        print("🤖 COMMENCING MULTI-REGISTER MATRIX VERIFICATION")
        print("==================================================")
        
        if not self.compile_cpp_engine():
            sys.exit(1)
            
        # 1. Gather Python Reference Ground Truth
        # Modify your prototype to run for the exact matching short tracking block
        py_results = self.validator.run_stress_test(total_steps=steps)
        py_coords = py_results["final_coords"]
        
        # 2. Gather Native Compiled C++ Results
        cpp_coords = self.run_cpp_engine(steps)
        
        if cpp_coords is None:
            print("❌ Verification Aborted: C++ binary output parsing failed.")
            sys.exit(1)
            
        # 3. Bit-for-Bit Assertion Check
        print("\n🔍 CROSS-EXAMINATION MATRIX:")
        print(f" -> Python Core Matrix Target : {py_coords}")
        print(f" -> C++ Native Production Out  : {cpp_coords}")
        
        if py_coords == cpp_coords:
            print("\n🎉 VERIFICATION SUCCESS: [M] and [E] Registers are perfectly in sync.")
            print("The shortcut optimization behaves identically across both layers.")
            return True
        else:
            print("\n❌ VERIFICATION FAILURE: Numeric drift or logical state mismatch detected.")
            print("Check step boundaries or integer casting inside the C++ bitwise loops.")
            return False

if __name__ == "__main__":
    # Point relative paths to your active workspace directories
    cpp_src = os.path.join(os.path.dirname(__file__), "../src/lattice_routing.cpp")
    cpp_bin = os.path.join(os.path.dirname(__file__), "../src/lattice_routing.bin")
    
    verifier = CrossLanguageVerifier(cpp_src, cpp_bin)
    # Run a localized 1,000-step cross-audit pass to confirm absolute logical alignment
    verifier.execute_cross_audit(steps=1000)

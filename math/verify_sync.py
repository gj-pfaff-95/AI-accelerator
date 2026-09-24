import subprocess
import sys
import os
from route_validator import LatticeRouteValidator

class CrossLanguageVerifier:
    def __init__(self, repo_root_path):
        self.repo_root = repo_root_path
        self.build_dir = os.path.join(repo_root_path, "build")
        
        # Resolve path configurations based on target OS parameters
        if sys.platform == "win32":
            self.cpp_binary = os.path.join(self.build_dir, "bin", "LatticeRoutingEngine.exe")
        else:
            self.cpp_binary = os.path.join(self.build_dir, "bin", "LatticeRoutingEngine")
            
        self.validator = LatticeRouteValidator()

    def compile_via_cmake(self):
        """Automates out-of-source CMake builds cleanly to bypass raw compiler platform bugs."""
        print(f"[M] Register: Initializing platform-native CMake build pipeline...")
        
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)
            
        gen_result = subprocess.run(["cmake", ".."], cwd=self.build_dir, capture_output=True, text=True)
        if gen_result.returncode != 0:
            print("❌ CMake generation pass failed:")
            print(gen_result.stderr)
            return False
            
        build_result = subprocess.run(["cmake", "--build", "."], cwd=self.build_dir, capture_output=True, text=True)
        if build_result.returncode != 0:
            print("❌ CMake compilation target execution failed:")
            print(build_result.stderr)
            return False
            
        print("✅ CMake build targets updated cleanly.")
        return True

    def run_cpp_engine(self, steps):
        """Executes the compiled C++ binary and extracts its final state coordinates."""
        print(f"[M] Register: Running C++ execution layer for {steps:,} steps...")
        if not os.path.exists(self.cpp_binary):
            print(f"❌ Error: Compiled execution binary missing at {self.cpp_binary}")
            return None
            
        result = subprocess.run([self.cpp_binary], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ C++ Execution Error:")
            print(result.stderr)
            return None
            
        # Parse coordinates from stdout (Format: "Updated packet coordinates: [X, Y, Z]")
        for line in result.stdout.splitlines():
            if "Updated packet coordinates:" in line:
                try:
                    coord_str = line.split("[")[1].split("]")[0]
                    return [int(c.strip()) for c in coord_str.split(",")]
                except IndexError:
                    print("❌ Error: Could not parse coordinate format from C++ stdout.")
                    return None
        return None

    def execute_cross_audit(self, steps=1000):
        """Compares the NumPy model outputs directly against the C++ binary results."""
        print("==================================================")
        print("🤖 COMMENCING MULTI-REGISTER MATRIX VERIFICATION")
        print("==================================================")
        
        if not self.compile_via_cmake():
            sys.exit(1)
            
        # 1. Gather NumPy Reference Ground Truth
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
    # Resolve the absolute project repository root workspace folder path
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    verifier = CrossLanguageVerifier(repo_root)
    verifier.execute_cross_audit(steps=1000)

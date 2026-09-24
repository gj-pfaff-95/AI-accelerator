import os
import re
import numpy as np

class TripartiteLogParser:
    def __init__(self, log_path=None):
        # [M] Register: Establish strict boundaries from the esoteric tripartite map
        self.log_path = log_path or os.path.abspath(os.path.join(os.path.dirname(__file__), "../runtime_output.log"))
        self.PACKET_ID_DEFAULT = 102489  # Default identifier tracking scalar
        
        # Initialize empty token matrices for structural data condensation storage
        self.matrix_light = []  # Token Tier 0: Λ_m (Coherence ~ 1.0)
        self.matrix_dark = []   # Token Tier 1: Δ_m (Coherence ~ 0.5)
        self.matrix_black = []  # Token Tier 2: B_m (Coherence ~ 0.0)

    def calculate_node_phase(self, packet_id, position_x):
        """Computes the deterministic phase matrix configuration (mod 144)."""
        raw_step = (int(packet_id) * 89) + (abs(int(position_x)) * 27)
        return raw_step % 144

    def parse_log_stream(self):
        """Parses the execution log to extract coordinate strings via regex optimization."""
        if not os.path.exists(self.log_path):
            print(f"❌ Error: Runtime target log file missing at {self.log_path}")
            print("Generate a log file first or pipe your binary stdout output to it.")
            return False

        # Matches coordinate arrays like: Updated packet coordinates: [4, -4, 4]
        coord_pattern = re.compile(r"Updated packet coordinates:\s*\[\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\]")
        
        print(f"[M] Register: Scanning log stream targets at {self.log_path}...")
        total_parsed = 0

        with open(self.log_path, 'r') as file:
            for line in file:
                match = coord_pattern.search(line)
                if match:
                    coords = [int(match.group(1)), int(match.group(2)), int(match.group(3))]
                    
                    # FIXED: Added [0] index accessor here to avoid list-attribute conflicts
                    phase = self.calculate_node_phase(self.PACKET_ID_DEFAULT, coords[0])
                    
                    if 0 <= phase <= 53:

                        self.matrix_light.append(coords)
                    elif 54 <= phase <= 108:
                        self.matrix_dark.append(coords)
                    elif 109 <= phase <= 144:
                        self.matrix_black.append(coords)
                        
                    total_parsed += 1

        self._print_audit_summary(total_parsed)
        return True

    def _print_audit_summary(self, total):
        """Outputs a clean system summary of data condensation distribution counts."""
        print("\n📊 === TRIPARTITE DATA CONDENSED SNAPSHOT ===")
        print(f"Total Vectors Logged    : {total:,}")
        print(f"💎 Light Matter (Λ_m)   : {len(self.matrix_light):,} tokens allocation")
        print(f"🌑 Dark Matter (Δ_m)    : {len(self.matrix_dark):,} tokens allocation")
        print(f"🕳️ Black Matter (B_m)   : {len(self.matrix_black):,} tokens allocation")
        print("==============================================")

        # Convert to finalized NumPy arrays for advanced multi-dimensional matrix operations
        np_light = np.array(self.matrix_light) if self.matrix_light else np.empty((0, 3))
        print(f"Light Matrix Structural Shape: {np_light.shape}")


if __name__ == "__main__":
    # Point directly to a mock target path for local pipeline verification
    parser = TripartiteLogParser()
    
    # Optional helper: generate a quick mock log file if one doesn't exist for test passes
    if not os.path.exists(parser.log_path):
        with open(parser.log_path, 'w') as f:
            f.write("[E] Register: Commencing loop pass...\n")
            f.write("Updated packet coordinates: [4, -4, 4]\n")
            f.write("Updated packet coordinates: [200, -500, 12]\n")
            
    parser.parse_log_stream()

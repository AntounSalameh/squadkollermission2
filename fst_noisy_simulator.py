"""
Mission 02: 04_fst_noisy_simulator.py
Station: Systems Architect
Officer: [                           ]
"""

import re
import random

class FSTDialogueManager:
    def __init__(self):
        self.state = 'INIT'
        self.slot_memory = {"destination": None, "speed": None, "clearance_code": None}
        self.noise_tokens = ["Banana", "Labyrinth", "Quantum", "Midnight", "Velocity", "Green", "Cosmological"]

    def apply_noisy_channel(self, text):
        """Applies Shannon's Noisy Channel constraints (max 7 words, 1 noise token)."""
        noise = random.choice(self.noise_tokens)
        words = text.split()
        
        # Reserve 1 spot for the noise token, max 6 words from original text
        if len(words) > 6:
            words = words[:6]
            
        words.append(f"{noise}.")
        return " ".join(words)

    def extract_slots(self, text):
        dest_match = re.search(r"(?i)(?:to|destination|for)\s+([a-zA-Z\s]+)", text)
        if dest_match:
            # Basic cleanup to avoid catching other parameters
            extracted = dest_match.group(1).split(" speed")[0].split(" warp")[0].split(" code")[0].strip()
            self.slot_memory['destination'] = extracted

        speed_match = re.search(r"(?i)(?:warp|speed)\s+(\d+)", text)
        if speed_match:
            self.slot_memory['speed'] = speed_match.group(1)

        code_match = re.search(r"(?i)(?:code|clearance)\s+([A-Z0-9]+)", text)
        if code_match:
            self.slot_memory['clearance_code'] = code_match.group(1)

    def process_input(self, user_input):
        response = ""

        if self.state == 'INIT':
            if 'wake' in user_input.lower() or 'system' in user_input.lower():
                self.state = 'GREETING'
                response = "System awake. Please state destination."
            else:
                response = "System idle. Awaiting wake word."

        elif self.state == 'GREETING':
            self.extract_slots(user_input)
            self.state = 'COLLECT_SLOTS'
            response = self.check_slots()

        elif self.state == 'COLLECT_SLOTS':
            self.extract_slots(user_input)
            response = self.check_slots()

        elif self.state == 'CONFIRMATION':
            if 'yes' in user_input.lower():
                self.state = 'TERMINAL'
                response = "Execution confirmed. Initiating subspace jump."
            elif 'no' in user_input.lower():
                self.slot_memory = {"destination": None, "speed": None, "clearance_code": None}
                self.state = 'COLLECT_SLOTS'
                response = "Slots cleared. State destination, speed, code."
            else:
                response = "Please confirm with yes or no."
        
        elif self.state == 'TERMINAL':
            response = "Session terminated. AURA system going offline."
        
        else:
            self.state = 'FALLBACK'
            response = "Error. State unknown. Resetting."
            self.state = 'INIT'

        return self.apply_noisy_channel(response)

    def check_slots(self):
        missing = [k for k, v in self.slot_memory.items() if v is None]
        if not missing:
            self.state = 'CONFIRMATION'
            return f"Confirm: {self.slot_memory['destination']}, W{self.slot_memory['speed']}, C{self.slot_memory['clearance_code']}?"
        else:
            return f"Missing parameters. Please provide: {', '.join(missing)}."

# Simulation Runner
if __name__ == "__main__":
    fst = FSTDialogueManager()
    
    # 10-turn transcript simulation
    turns = [
        "System wake up.",
        "Destination Sirius B",
        "Warp 5",
        "Code ALPHA",
        "No wait, change destination to Mars.",
        "Destination Mars",
        "Speed Banana",
        "Warp 7",
        "Code OMEGA",
        "Yes"
    ]

    print("--- NOISY INTERROGATION TRANSCRIPT ---")
    for i, user_turn in enumerate(turns, 1):
        print(f"Turn {i} - User: {user_turn}")
        sys_resp = fst.process_input(user_turn)
        print(f"Turn {i} - System (State: {fst.state}): {sys_resp}\n")

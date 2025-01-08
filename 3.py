import math
import cmath

class UnifiedForce:
    def __init__(self):
        self.phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        self.coulomb = 1.602176634e-19  # Charge of an electron in Coulombs
        self.ohm = 1.0  # Base resistance, adjust as needed
        self.state_properties = {
            'solid': {'rho': 1.0, 'Y': 100.0},  
            'liquid': {'rho': 0.8, 'kappa': 2.0},
            'gas': {'rho': 0.001, 'c_s': 343},  
            'plasma': {'n_e': 1e20, 'e': self.coulomb, 'epsilon_0': 8.854187817e-12, 'm_e': 9.10938356e-31}
        }

    def fibonacci(self, n):
        """Generate the nth Fibonacci number."""
        return 0 if n <= 0 else 1 if n == 1 else self.fibonacci(n - 1) + self.fibonacci(n - 2)

    def prime(self, n):
        """Generate the nth prime number."""
        primes = []
        num = 2
        while len(primes) < n:
            if all(num % p > 0 for p in primes):
                primes.append(num)
            num += 1
        return primes[-1]

    def state_resistance(self, state: str) -> float:
        """Return a state-specific resistance coefficient."""
        props = self.state_properties.get(state)
        if state == 'solid':
            return props['rho'] * props['Y']
        elif state == 'liquid':
            return props['rho'] * props['kappa']
        elif state == 'gas':
            return props['rho'] * props['c_s']**2
        elif state == 'plasma':
            return (props['n_e'] * props['e']**2) / (props['epsilon_0'] * props['m_e'])
        else:
            raise ValueError("Invalid state provided")

    def state_scaling(self, state: str) -> tuple:
        """Return state-specific scaling factors for meters and seconds."""
        scale_factors = {
            'solid': (1.0, 1.0),
            'liquid': (0.9, 0.95),
            'gas': (0.5, 0.01),
            'plasma': (10.0, 1.0)
        }
        return scale_factors.get(state, (1.0, 1.0))

    def force_unified(self, states: list, meters: float, seconds: float, n: int) -> float:
        """Calculate the unified force for given states."""
        sum_term = 0
        for state in states:
            phi_i = self.phi
            F_n_i = self.fibonacci(n)
            P_n_i = self.prime(n)
            Omega_i = self.state_resistance(state)
            m_s, s_s = self.state_scaling(state)
            X_i_state = self.state_resistance(state)
            
            sum_term += phi_i * (F_n_i ** n) * P_n_i * Omega_i * (1 / (meters * m_s)**2) * X_i_state
        
        return sum_term / (seconds * s_s)

    def frequency_unified(self, states: list, meters: float, n: int) -> float:
        """Calculate the unified frequency for given states."""
        sum_term = 0
        for state in states:
            phi_i = self.phi
            F_n_i = self.fibonacci(n)
            P_n_i = self.prime(n)
            Omega_i = self.state_resistance(state)
            r_i = meters  
            X_i_state = self.state_resistance(state)
            
            sum_term += phi_i * (F_n_i ** n) * P_n_i * Omega_i * (1 / r_i**2) * X_i_state
        
        return math.sqrt(sum_term)

    def force_to_frequency(self, force: float, meters: float, seconds: float) -> float:
        """Convert force to frequency squared."""
        return math.sqrt(force * (meters * seconds))

    def euler_relation(self) -> bool:
        """Check Euler's relation with resistance."""
        return math.isclose(cmath.exp(1j * math.pi).real, -1) and \
               math.isclose(self.ohm * self.coulomb**2, 1)

    def simulate_scenario(self, states: list, meters: float, seconds: float, n: int) -> dict:
        """Simulate a scenario and return all calculated values."""
        force = self.force_unified(states, meters, seconds, n)
        frequency = self.frequency_unified(states, meters, n)
        freq_from_force = self.force_to_frequency(force, meters, seconds)
        euler_check = self.euler_relation()
        
        return {
            'Force': force,
            'Frequency': frequency,
            'Frequency from Force': freq_from_force,
            'Euler Relation Valid': euler_check
        }

    def modify_state_property(self, state: str, property: str, value: float):
        """Modify a state property for simulation purposes."""
        if state in self.state_properties and property in self.state_properties[state]:
            self.state_properties[state][property] = value
        else:
            raise ValueError(f"Invalid state or property: {state}, {property}")

if __name__ == "__main__":
    unified_force = UnifiedForce()

    while True:
        print("\nUnified Force Framework Simulator")
        print("1. Run Simulation")
        print("2. Modify State Property")
        print("3. View State Properties")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            states = input("Enter states (comma separated, e.g., solid,liquid,gas,plasma): ").split(',')
            meters = float(input("Enter distance in meters: "))
            seconds = float(input("Enter time in seconds: "))
            n = int(input("Enter the Fibonacci/Prime index n: "))
            
            results = unified_force.simulate_scenario(states, meters, seconds, n)
            for key, value in results.items():
                print(f"{key}: {value}")
        
        elif choice == '2':
            state = input("Enter state to modify (solid, liquid, gas, or plasma): ").strip().lower()
            property = input("Enter property to modify (e.g., rho, Y, kappa, c_s, n_e, e, epsilon_0, m_e): ").strip().lower()
            value = float(input("Enter new value: "))
            try:
                unified_force.modify_state_property(state, property, value)
                print(f"Property '{property}' for state '{state}' updated to {value}.")
            except ValueError as e:
                print(str(e))
        
        elif choice == '3':
            for state, props in unified_force.state_properties.items():
                print(f"{state.capitalize()}:")
                for prop, val in props.items():
                    print(f"  {prop}: {val}")
        
        elif choice == '4':
            print("Exiting the simulator. Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")
import random

class UrbanServiceModel:
    """Model public service provision and social infrastructure in Bangladesh cities (Focus: Edu, Health, Public Space)"""
    def __init__(self, config):
        self.school_density = config['service_delivery']['school_density'].copy() # Schools per sq km
        self.hospital_beds = config['service_delivery']['hospital_beds_per_1000'].copy() # Beds per 1000 pop
        self.public_space_pc = config['service_delivery']['public_space_per_capita'].copy() # sq m per capita
        self.current_year = 2025
        print("UrbanServiceModel Initialized")

    def simulate_step(self, year, population_data, governance_data):
        """Simulates changes in social infrastructure provision levels."""
        print(f"  Simulating Urban Service (Social Infra) Dynamics for year {year}...")

        for city in self.school_density: # Assuming keys exist for all tracked metrics
            # Factors: Population growth (demand), municipal investment (revenue/governance), land availability (growth model - TBD)

            revenue_factor = governance_data.get('own_revenue', {}).get(city, 0.3) / 0.3 # Relative revenue
            # Need population growth rate for per-capita adjustments
            # Placeholder for population growth calculation (requires storing previous year pop)
            pop_now = population_data.get(city, 1000000)
            # pop_prev = ...
            # pop_growth_rate = (pop_now - pop_prev) / pop_prev if pop_prev else 0
            pop_growth_rate = 0.03 # Using fixed rate for now

            # --- School Density ---
            # Assume investment leads to new schools, increasing density
            school_investment_rate = random.uniform(0.002, 0.008) * revenue_factor
            self.school_density[city] = self.school_density.get(city, 4) * (1 + school_investment_rate)

            # --- Hospital Beds per 1000 ---
            # Investment increases total beds, but rate per 1000 depends on population growth
            bed_investment_rate = random.uniform(0.003, 0.01) * revenue_factor
            current_beds_pc = self.hospital_beds.get(city, 1.5)
            # Calculate new total beds based on old rate and pop, add new beds, then recalculate per capita
            # total_beds_old = current_beds_pc * (pop_now / (1 + pop_growth_rate)) / 1000
            # new_total_beds = total_beds_old * (1 + bed_investment_rate)
            # self.hospital_beds[city] = (new_total_beds / pop_now) * 1000
            # Simplified: Adjust rate directly, implicitly accounting for pop growth effect
            self.hospital_beds[city] = current_beds_pc * (1 + bed_investment_rate - pop_growth_rate * 0.5) # Growth dilutes per capita rate
            self.hospital_beds[city] = max(0.5, self.hospital_beds[city]) # Floor

            # --- Public Space Per Capita ---
            # New space development vs population growth pressure
            space_development_rate = random.uniform(0.001, 0.005) * revenue_factor # Rate of new space addition relative to existing
            current_space_pc = self.public_space_pc.get(city, 1.0)
            # Similar logic to beds: calculate total, add new, recalculate per capita
            # Simplified: Adjust rate directly
            self.public_space_pc[city] = current_space_pc * (1 + space_development_rate - pop_growth_rate)
            self.public_space_pc[city] = max(0.2, self.public_space_pc[city]) # Floor value

        print(f"    Dhaka Hospital Beds per 1000 Estimate: {self.hospital_beds.get('Dhaka', 'N/A'):.2f}")
        print(f"    Chattogram Public Space per Capita Estimate: {self.public_space_pc.get('Chattogram', 'N/A'):.2f}")
        self.current_year = year

    def get_service_state(self):
        return {
            'school_density': self.school_density,
            'hospital_beds_per_1000': self.hospital_beds,
            'public_space_per_capita': self.public_space_pc
        } 
import random

class UrbanGovernanceModel:
    """Model governance frameworks and planning systems for Bangladesh cities"""
    def __init__(self, config):
        self.own_revenue = config['governance']['municipal_own_revenue'].copy() # % of total budget
        self.satisfaction = config['governance']['citizen_satisfaction'].copy() # Index 0-1
        self.compliance = config['governance']['planning_compliance'].copy() # % development adhering to plan
        self.current_year = 2025
        print("UrbanGovernanceModel Initialized")

    def simulate_step(self, year, infrastructure_data, social_data):
        """Simulates changes in governance indicators like revenue, satisfaction, and compliance."""
        print(f"  Simulating Governance Dynamics for year {year}...")

        for city in self.satisfaction: # Assuming keys exist for all tracked metrics
            # --- Citizen Satisfaction ---
            # Factors: Service levels (infra), social conditions (cohesion, crime), maybe transparency/participation (TBD)
            # Simple average of key service coverages
            avg_infra_coverage = (
                infrastructure_data.get('water_coverage', {}).get(city, 0.5) +
                infrastructure_data.get('sanitation_coverage', {}).get(city, 0.5) +
                infrastructure_data.get('power_reliability', {}).get(city, 0.8) +
                infrastructure_data.get('waste_collection', {}).get(city, 0.5)
            ) / 4

            # Social factors (e.g., cohesion improvement, crime reduction)
            cohesion_level = social_data.get('cohesion', {}).get(city, 0.6)
            crime_level_factor = 1 - (social_data.get('crime_rate', {}).get(city, 250) / 300) # Inverse relationship relative to Dhaka start

            satisfaction_change = (
                (avg_infra_coverage - 0.65) * 0.05 + # Driven by infrastructure level vs a baseline
                (cohesion_level - 0.6) * 0.03 + # Driven by social cohesion vs baseline
                (crime_level_factor - 0.0) * 0.02 # Driven by crime reduction
                 + random.uniform(-0.015, 0.015) # Random fluctuation
            )
            self.satisfaction[city] = max(0.1, min(0.9, self.satisfaction.get(city, 0.5) + satisfaction_change))

            # --- Municipal Own Revenue ---
            # Factors: Economic growth (tax base), collection efficiency (institutional capacity - TBD)
            # Placeholder: Slight increase linked to GDP growth
            # gdp_growth = economy_data... # Needs economy data passed in
            revenue_change = random.uniform(0.001, 0.01) # Slow base increase
            self.own_revenue[city] = min(0.8, max(0.1, self.own_revenue.get(city, 0.3) * (1 + revenue_change)))

            # --- Planning Compliance ---
            # Factors: Enforcement capacity (institutional), development pressure (growth), citizen awareness (satisfaction?)
            # Placeholder: Slight random fluctuation, maybe higher compliance if satisfaction is high?
            compliance_change = random.uniform(-0.01, 0.01) + (self.satisfaction[city] - 0.5)*0.01
            self.compliance[city] = min(0.9, max(0.2, self.compliance.get(city, 0.45) * (1 + compliance_change)))

        print(f"    Dhaka Citizen Satisfaction Estimate: {self.satisfaction.get('Dhaka', 'N/A'):.2f}")
        print(f"    Chattogram Planning Compliance Estimate: {self.compliance.get('Chattogram', 'N/A'):.2f}")
        self.current_year = year

    def get_governance_state(self):
        return {
            'municipal_own_revenue': self.own_revenue,
            'citizen_satisfaction': self.satisfaction,
            'planning_compliance': self.compliance
        } 
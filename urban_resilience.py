import random

class UrbanResilienceModel:
    """Model risk reduction and resilience building in Bangladesh cities"""
    def __init__(self, config):
        self.warning_coverage = config['resilience']['early_warning_coverage'].copy() # % pop covered
        self.code_compliance = config['resilience']['building_code_compliance'].copy() # % new builds
        self.recovery_speed = config['resilience']['disaster_recovery_speed'].copy() # Avg time (days), lower is better
        self.current_year = 2025
        print("UrbanResilienceModel Initialized")

    def simulate_step(self, year, governance_data, environment_data):
        """Simulates changes in resilience indicators like warning coverage, compliance, and recovery speed."""
        print(f"  Simulating Urban Resilience Dynamics for year {year}...")

        for city in self.warning_coverage: # Assuming keys exist for all tracked metrics
            # --- Early Warning Coverage ---
            # Factors: Investment (governance), technology adoption (smart city - TBD)
            # Placeholder: Assume steady improvement, maybe faster in more flood-prone areas
            investment_factor = governance_data.get('own_revenue', {}).get(city, 0.3) / 0.3
            flood_prone_factor = environment_data.get('flood_prone', {}).get(city, 0.2) / 0.2 # Higher if more prone

            coverage_increase = random.uniform(0.01, 0.03) * investment_factor * (1 + flood_prone_factor * 0.5)
            self.warning_coverage[city] = min(1.0, self.warning_coverage.get(city, 0.7) * (1 + coverage_increase))

            # --- Building Code Compliance ---
            # Factors: Governance (planning compliance, enforcement capacity - TBD), awareness (social - TBD)
            planning_compliance_factor = governance_data.get('compliance', {}).get(city, 0.5)
            compliance_increase = random.uniform(0.005, 0.015) * planning_compliance_factor # Driven by general planning compliance
            self.code_compliance[city] = min(0.95, self.code_compliance.get(city, 0.5) * (1 + compliance_increase))

            # --- Disaster Recovery Speed (Days) ---
            # Factors: Infrastructure resilience (TBD), institutional capacity (governance), social cohesion (social)
            # Lower number is better
            governance_factor = governance_data.get('satisfaction', {}).get(city, 0.5) # Proxy for capacity
            social_cohesion_factor = 1.0 # Needs social_data passed in
            # infrastructure_resilience_factor = ...

            # Improvement means reducing the number of days
            speed_improvement_rate = random.uniform(0.01, 0.04) * governance_factor # * social_cohesion_factor
            self.recovery_speed[city] = self.recovery_speed.get(city, 10) * (1 - speed_improvement_rate)
            self.recovery_speed[city] = max(1, self.recovery_speed[city]) # Minimum 1 day recovery

        print(f"    Chattogram Building Code Compliance Estimate: {self.code_compliance.get('Chattogram', 'N/A'):.2f}")
        print(f"    Khulna Disaster Recovery Speed Estimate: {self.recovery_speed.get('Khulna', 'N/A'):.1f} days")
        self.current_year = year

    def get_resilience_state(self):
        return {
            'early_warning_coverage': self.warning_coverage,
            'building_code_compliance': self.code_compliance,
            'disaster_recovery_speed': self.recovery_speed
        } 
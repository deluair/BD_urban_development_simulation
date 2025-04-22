import random

class UrbanSocialModel:
    """Model social structures, cultural patterns and community dynamics in Bangladesh cities"""
    def __init__(self, config):
        self.literacy = config['social']['literacy_rate'].copy()
        self.healthcare_access = config['social']['access_to_healthcare'].copy()
        self.cohesion = config['social']['social_cohesion_index'].copy()
        self.crime_rate = config['social']['crime_rate'].copy() # Per 100k pop
        self.current_year = 2025
        print("UrbanSocialModel Initialized")

    def simulate_step(self, year, population_data, economy_data, governance_data, service_data):
        """Simulates changes in literacy, health access, cohesion, and crime rates."""
        print(f"  Simulating Social Dynamics for year {year}...")

        for city in self.literacy: # Assuming keys exist for all tracked metrics
            # --- Literacy Rate ---
            # Factors: Education service availability (service model), economic conditions (affordability - TBD)
            school_density_factor = service_data.get('school_density', {}).get(city, 4) / 4 # Relative to Chattogram start
            literacy_change = random.uniform(0.003, 0.008) * school_density_factor # Base improvement driven by school density
            self.literacy[city] = min(0.98, self.literacy.get(city, 0.7) * (1 + literacy_change))

            # --- Healthcare Access ---
            # Factors: Healthcare service availability (service model - beds/facility density)
            hospital_beds_factor = service_data.get('hospital_beds_per_1000', {}).get(city, 1.5) / 1.5 # Relative to Chattogram start
            health_access_change = random.uniform(0.004, 0.012) * hospital_beds_factor
            self.healthcare_access[city] = min(0.99, self.healthcare_access.get(city, 0.8) * (1 + health_access_change))

            # --- Social Cohesion ---
            # Factors: Inequality (economy - TBD), governance satisfaction, crime rate (inverse), migration (potentially negative initially)
            satisfaction_factor = governance_data.get('satisfaction', {}).get(city, 0.5)
            # Placeholder for inequality effect
            # inequality_factor = ...
            crime_factor = 1 - (self.crime_rate.get(city, 250) / 500) # Higher crime reduces cohesion (relative to higher bound)
            # Placeholder for migration effect
            # migration_factor = ...

            cohesion_change = (
                (satisfaction_factor - 0.5) * 0.03 + # Higher satisfaction boosts cohesion
                (crime_factor - 0.5) * 0.02 + # Lower crime boosts cohesion
                random.uniform(-0.01, 0.01)
            )
            self.cohesion[city] = max(0.2, min(0.9, self.cohesion.get(city, 0.6) + cohesion_change))

            # --- Crime Rate ---
            # Factors: Unemployment (economy), social cohesion (inverse), inequality (TBD), density (TBD), policing (governance - TBD)
            unemployment_factor = economy_data.get('unemployment', {}).get(city, 0.07) / 0.07 # Relative to 7%
            cohesion_factor = (1 - self.cohesion[city]) / 0.5 # Inverse, relative to 0.5 baseline cohesion
            # density_factor = ...

            crime_rate_change_multiplier = (
                1 +
                (unemployment_factor - 1) * 0.05 + # Higher unemployment increases crime rate % change
                (cohesion_factor - 1) * 0.03 + # Lower cohesion increases crime rate % change
                random.uniform(-0.02, 0.02)
            )
            self.crime_rate[city] = max(50, self.crime_rate.get(city, 250) * crime_rate_change_multiplier)

        print(f"    Dhaka Literacy Rate Estimate: {self.literacy.get('Dhaka', 'N/A'):.2f}")
        print(f"    Khulna Social Cohesion Index Estimate: {self.cohesion.get('Khulna', 'N/A'):.2f}")
        print(f"    Dhaka Crime Rate Estimate: {self.crime_rate.get('Dhaka', 'N/A'):.0f}")
        self.current_year = year

    def get_social_state(self):
        return {
            'literacy': self.literacy,
            'healthcare_access': self.healthcare_access,
            'cohesion': self.cohesion,
            'crime_rate': self.crime_rate
        } 
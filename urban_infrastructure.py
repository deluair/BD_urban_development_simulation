import random

class UrbanInfrastructureModel:
    """Model infrastructure networks and service delivery in Bangladesh cities"""
    def __init__(self, config):
        self.water_coverage = config['infrastructure']['water_coverage'].copy()
        self.sanitation_coverage = config['infrastructure']['sanitation_coverage'].copy()
        self.power_reliability = config['infrastructure']['power_reliability'].copy()
        self.waste_collection = config['infrastructure']['waste_collection'].copy()
        self.internet_penetration = config['infrastructure']['internet_penetration'].copy()
        self.current_year = 2025
        print("UrbanInfrastructureModel Initialized")

    def simulate_step(self, year, population_data, governance_data):
        """Simulates the improvement or degradation of infrastructure coverage/quality."""
        print(f"  Simulating Infrastructure Dynamics for year {year}...")

        for city in self.water_coverage: # Assuming keys exist for all tracked metrics
            # Factors influencing infrastructure improvement:
            # - Population Growth (increases strain, may slow coverage % increase)
            # - Municipal Revenue/Investment (governance)
            # - Base level (diminishing returns as coverage approaches 100%)

            pop_growth_factor = (population_data.get(city, 1) / population_data.get(city, 1)) -1 # Need previous year pop or calculate growth
            # For simplicity now, just use a small negative effect if pop grows
            pop_strain = population_data.get(city, 1000000) > 1000000 # Example simple check

            investment_factor = governance_data.get('own_revenue', {}).get(city, 0.3) / 0.3 # Relative revenue

            # Water Coverage
            base_improvement = random.uniform(0.005, 0.02)
            current_coverage = self.water_coverage[city]
            improvement = base_improvement * investment_factor * (1 - current_coverage) # Diminishing returns
            improvement *= (0.95 if pop_strain else 1.0) # Apply strain factor
            self.water_coverage[city] = min(1.0, current_coverage + improvement)

            # Sanitation Coverage
            base_improvement = random.uniform(0.004, 0.018)
            current_coverage = self.sanitation_coverage.get(city, 0.5)
            improvement = base_improvement * investment_factor * (1 - current_coverage)
            improvement *= (0.90 if pop_strain else 1.0) # Sanitation potentially more strained
            self.sanitation_coverage[city] = min(1.0, current_coverage + improvement)

            # Power Reliability
            base_improvement = random.uniform(0.002, 0.01)
            current_level = self.power_reliability.get(city, 0.8)
            improvement = base_improvement * investment_factor * (1 - current_level)
            improvement *= (0.97 if pop_strain else 1.0)
            self.power_reliability[city] = min(1.0, current_level + improvement)

            # Waste Collection
            base_improvement = random.uniform(0.005, 0.02)
            current_coverage = self.waste_collection.get(city, 0.5)
            improvement = base_improvement * investment_factor * (1 - current_coverage)
            improvement *= (0.90 if pop_strain else 1.0)
            self.waste_collection[city] = min(1.0, current_coverage + improvement)

            # Internet Penetration (driven more by private sector/national policy but influenced by demand/urbanization)
            base_improvement = random.uniform(0.02, 0.05)
            current_coverage = self.internet_penetration.get(city, 0.5)
            improvement = base_improvement * (1 - current_coverage) # Less dependent on local gov revenue
            self.internet_penetration[city] = min(1.0, current_coverage + improvement)


        print(f"    Dhaka Water Coverage Estimate: {self.water_coverage.get('Dhaka', 'N/A'):.2f}")
        print(f"    Khulna Sanitation Coverage Estimate: {self.sanitation_coverage.get('Khulna', 'N/A'):.2f}")
        self.current_year = year

    def get_infrastructure_state(self):
        """Returns the current state of all infrastructure metrics."""
        return {
            'water_coverage': self.water_coverage,
            'sanitation_coverage': self.sanitation_coverage,
            'power_reliability': self.power_reliability,
            'waste_collection': self.waste_collection,
            'internet_penetration': self.internet_penetration,
        } 
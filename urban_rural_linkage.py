import random

class UrbanRuralLinkageModel:
    """Model interconnections between urban centers and rural hinterlands in Bangladesh"""
    def __init__(self, config):
        self.remittance_dep = config['urban_rural']['remittance_dependency'].copy() # % hh income (static for now)
        self.migration_rate = config['urban_rural']['rural_migration_rate'].copy() # Net annual % into major cities
        self.commuter_perc = config['urban_rural']['commuter_percentage'].copy() # % workforce commuting
        self.current_year = 2025
        print("UrbanRuralLinkageModel Initialized")

    def simulate_step(self, year, economy_data, transport_data, housing_data):
        """Simulates changes in migration rates and commuting patterns."""
        print(f"  Simulating Urban-Rural Linkages for year {year}...")

        # Note: Migration rate here is net inflow *to the city*. A full model would track rural population too.
        # Remittance dependency is currently static - would need rural income/urban wage data.

        for city in self.migration_rate: # Simulate for cities where migration is tracked
            # --- Net Migration Rate Adjustment ---
            # Factors: Urban economic opportunity (GDP growth, unemployment - inverse), rural conditions (TBD),
            #          housing affordability (inverse), potential network effects

            urban_unemployment = economy_data.get('unemployment', {}).get(city, 0.07)
            # Placeholder for GDP growth pull factor
            # urban_gdp_growth = ...
            urban_affordability_ratio = housing_data.get('affordability', {}).get(city, 15)

            # Higher unemployment reduces pull factor
            unemployment_effect = (urban_unemployment / 0.06 - 1) * -0.1 # Reduces migration if unemployment > 6%
            # Lower affordability reduces pull factor
            affordability_effect = (urban_affordability_ratio / 12 - 1) * -0.05 # Reduces migration if ratio > 12

            migration_rate_change = unemployment_effect + affordability_effect + random.uniform(-0.002, 0.002)
            self.migration_rate[city] = self.migration_rate.get(city, 0.01) * (1 + migration_rate_change)
            self.migration_rate[city] = max(0.001, min(0.05, self.migration_rate[city])) # Bounds on net inflow rate

        for city in self.commuter_perc:
            # --- Commuter Percentage Adjustment ---
            # Factors: Transport conditions (commute time - inverse), housing affordability (direct - push factor),
            #          job availability in city (direct)

            avg_commute_time = transport_data.get('avg_commute_time', {}).get(city, 60)
            urban_affordability_ratio = housing_data.get('affordability', {}).get(city, 15)

            commute_time_effect = (avg_commute_time / 50 - 1) * -0.02 # Less commuting if time > 50 mins
            affordability_effect = (urban_affordability_ratio / 12 - 1) * 0.03 # More commuting if ratio > 12

            commuter_perc_change = commute_time_effect + affordability_effect + random.uniform(-0.005, 0.005)
            self.commuter_perc[city] = self.commuter_perc.get(city, 0.1) * (1 + commuter_perc_change)
            self.commuter_perc[city] = max(0.05, min(0.4, self.commuter_perc[city])) # Bounds 5% - 40%

        print(f"    Dhaka Net Rural Migration Rate Estimate: {self.migration_rate.get('Dhaka', 'N/A'):.3f}")
        print(f"    Dhaka Commuter Percentage Estimate: {self.commuter_perc.get('Dhaka', 'N/A'):.2f}")
        self.current_year = year

    def get_linkage_state(self):
        return {
            'remittance_dependency': self.remittance_dep,
            'migration_rate': self.migration_rate,
            'commuter_percentage': self.commuter_perc
        } 
import random

class UrbanGrowthModel:
    """Model urban expansion patterns and spatial transformation in Bangladesh"""
    def __init__(self, config):
        self.population = config['urban_growth']['initial_population'].copy()
        self.growth_rate = config['urban_growth']['annual_growth_rate']
        # Store land use data per city - more complex structure might be needed later
        self.land_use = config['urban_growth']['land_use'].copy()
        self.peri_urban = config['urban_growth']['peri_urban_areas']
        self.current_year = 2025
        print("UrbanGrowthModel Initialized")

    def simulate_step(self, year):
        """Simulates population growth and basic land use pressure for one year."""
        print(f"  Simulating Urban Growth for year {year}...")
        cities_to_simulate = list(self.population.keys()) # Simulate for cities with initial population

        for city in cities_to_simulate:
            pop = self.population[city]
            rate = self.growth_rate.get(city, 0.02) # Use specific rate or default
            natural_increase = pop * (rate * 0.6) # Example: 60% of growth is natural
            migration = pop * (rate * 0.4) # Example: 40% is migration (could link to rural model later)

            # Add stochasticity
            growth_variation = random.normalvariate(1, 0.05) # +/- 5% variation around the rate
            new_pop = pop + (natural_increase + migration) * growth_variation
            self.population[city] = max(0, int(new_pop)) # Ensure population doesn't go negative

            # --- Placeholder Land Use Change ---
            # Needs more sophisticated spatial representation (e.g., grid, zones)
            # For now, just track % changes based on pop pressure
            if city in self.land_use:
                pop_increase_fraction = (self.population[city] - pop) / pop if pop > 0 else 0
                if pop_increase_fraction > 0:
                    # Assume increased demand for residential/informal
                    demand_factor = pop_increase_fraction * 0.1 # How much land % changes relative to pop % change

                    convertible_land = self.land_use[city].get('green', 0) # Prioritize converting green first

                    conversion_amount = min(convertible_land, self.land_use[city].get('green', 0) * demand_factor * 2) # Convert up to demand*2 from green

                    if conversion_amount > 0:
                         self.land_use[city]['green'] = self.land_use[city].get('green', 0) - conversion_amount
                         # Distribute converted land (example: 70% informal, 30% residential)
                         self.land_use[city]['informal'] = self.land_use[city].get('informal', 0) + conversion_amount * 0.7
                         self.land_use[city]['residential'] = self.land_use[city].get('residential', 0) + conversion_amount * 0.3
                         # Ensure percentages roughly sum to 100 (crude normalization)
                         total_land = sum(self.land_use[city].values())
                         if total_land > 0:
                             for use, percent in self.land_use[city].items():
                                 self.land_use[city][use] = (percent / total_land) * 100


        print(f"    Dhaka Population Estimate: {self.population.get('Dhaka', 'N/A')}")
        if 'Dhaka' in self.land_use:
             print(f"    Dhaka Land Use Estimate (Green%): {self.land_use['Dhaka'].get('green', 'N/A'):.1f}")
        self.current_year = year

    def get_population(self):
        return self.population

    def get_land_use(self):
        return self.land_use 
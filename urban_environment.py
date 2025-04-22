import random

class UrbanEnvironmentModel:
    """Model environmental systems and sustainability in Bangladesh cities"""
    def __init__(self, config):
        self.aqi = config['environment']['air_quality_index'].copy()
        self.green_space = config['environment']['green_space_ratio'].copy() # % land area
        self.flood_prone = config['environment']['flood_prone_area'].copy() # % land area (static for now)
        self.recycling_rate = config['environment']['waste_recycling_rate'].copy() # %
        self.current_year = 2025
        print("UrbanEnvironmentModel Initialized")

    def simulate_step(self, year, population_data, transport_data, land_use_data, infrastructure_data):
        """Simulates changes in environmental indicators like AQI, green space, recycling."""
        print(f"  Simulating Environmental Dynamics for year {year}...")

        for city in self.aqi: # Assuming keys exist for all tracked metrics
            # --- Air Quality Index (AQI) ---
            # Factors: Traffic (commute time/vehicles), industrial activity (economy - TBD), population density, green space (mitigation)
            pop_density_factor = population_data.get(city, 1000000) / 10000000 # Relative to 10M
            commute_factor = transport_data.get('avg_commute_time', {}).get(city, 60) / 60 # Relative to 60 mins
            # Placeholder for industrial effect (needs economy data)
            # industry_factor = economy_data.get('sectoral_employment', {}).get(city, {}).get('industry', 30) / 30
            green_space_mitigation = (1 - self.green_space.get(city, 0.05) / 0.1) # Lower AQI if green space > 10%

            aqi_change = (
                pop_density_factor * random.uniform(2, 5) + # Density contribution
                commute_factor * random.uniform(1, 4) + # Traffic contribution
                # industry_factor * random.uniform(1, 3) +
                - green_space_mitigation * random.uniform(0, 2) # Green space reduction
            )
            self.aqi[city] = max(30, self.aqi.get(city, 150) + aqi_change)

            # --- Green Space Ratio ---
            # Factors: Land conversion pressure (from growth model/land use)
            # Updated based on land use changes passed from UrbanGrowthModel (or directly here)
            if city in land_use_data:
                 current_green_percentage = land_use_data[city].get('green', self.green_space.get(city, 5))
                 self.green_space[city] = current_green_percentage # Update based on land use model results
            else:
                 # Fallback: slight decrease if not driven by land use model
                 self.green_space[city] = self.green_space.get(city, 0.05) * (1 - random.uniform(0.001, 0.005))
                 self.green_space[city] = max(0.01, self.green_space[city]) # Minimum green space

            # --- Recycling Rate ---
            # Factors: Waste collection efficiency (infra), policy/incentives (governance - TBD), citizen behaviour (social - TBD)
            collection_factor = infrastructure_data.get('waste_collection', {}).get(city, 0.6) / 0.6
            recycling_change = random.uniform(0.005, 0.02) * collection_factor # Higher collection enables better recycling
            self.recycling_rate[city] = min(0.6, self.recycling_rate.get(city, 0.1) * (1 + recycling_change))

            # --- Flood Prone Area --- (Considered static for now)
            # Could be dynamic based on climate change impacts (resilience model) or drainage improvements (infra)

        print(f"    Dhaka AQI Estimate: {self.aqi.get('Dhaka', 'N/A'):.0f}")
        print(f"    Chattogram Green Space Ratio Estimate: {self.green_space.get('Chattogram', 'N/A'):.3f}")
        self.current_year = year

    def get_environment_state(self):
        return {
            'aqi': self.aqi,
            'green_space': self.green_space,
            'flood_prone': self.flood_prone,
            'recycling_rate': self.recycling_rate
        } 
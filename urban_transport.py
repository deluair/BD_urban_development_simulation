import random

class UrbanTransportModel:
    """Model transportation systems and mobility patterns in Bangladesh cities"""
    def __init__(self, config):
        self.modal_split = config['transport']['modal_split'].copy()
        self.avg_commute_time = config['transport']['avg_commute_time'].copy()
        self.road_density = config['transport']['road_density'].copy() # km/sq km
        self.public_transit_coverage = config['transport']['public_transit_coverage'].copy() # % pop with access
        self.current_year = 2025
        print("UrbanTransportModel Initialized")

    def simulate_step(self, year, population_data, infrastructure_data, land_use_data):
        """Simulates changes in commute times and modal split based on urban factors."""
        print(f"  Simulating Transport Dynamics for year {year}...")

        for city in self.avg_commute_time:
            # --- Commute Time Adjustment ---
            # Factors: Population density, road density, public transit availability, maybe land use mix

            # Estimate population density (requires city area - placeholder)
            # Placeholder area calculation - assumes population is proportional to area initially
            # This needs a proper spatial component or area data in config
            initial_pop_dhaka = 18_000_000
            current_pop_dhaka = population_data.get('Dhaka', initial_pop_dhaka)
            # Assume Dhaka area ~300 sq km (very rough)
            estimated_area = 300 * (population_data.get(city, initial_pop_dhaka) / initial_pop_dhaka)
            pop_density = population_data.get(city, 1000000) / max(1, estimated_area) # Pop per sq km

            density_factor = pop_density / 60000 # Relative density compared to Dhaka initial estimate
            road_factor = self.road_density.get(city, 10) / 15 # Relative road density compared to Dhaka
            transit_factor = self.public_transit_coverage.get(city, 0.4) # Higher coverage should reduce time

            # Base change + density effect - road effect - transit effect
            commute_change_rate = (random.uniform(0.005, 0.02) # Base increase
                                 + density_factor * 0.03 # Density increases time
                                 - (road_factor - 1) * 0.01 # Higher road density slightly decreases time
                                 - (transit_factor - 0.4) * 0.02) # Higher transit coverage decreases time

            self.avg_commute_time[city] *= (1 + commute_change_rate)
            self.avg_commute_time[city] = max(15, self.avg_commute_time[city]) # Floor at 15 mins

            # --- Modal Split Adjustment --- (Highly simplified)
            # Shift away from walking/rickshaw towards bus/car if transit improves or commute time is high
            split = self.modal_split.get(city)
            if split:
                transit_improvement_factor = (self.public_transit_coverage.get(city, 0.4) - 0.4) * 0.1
                congestion_factor = (self.avg_commute_time[city] / 60 - 1) * 0.05 # Shift if commute > 60 mins

                # Shift from walk/rickshaw
                shift_away = (split['walk'] * (congestion_factor + transit_improvement_factor * 0.5) +
                              split['rickshaw'] * (congestion_factor*0.5 + transit_improvement_factor * 0.8)) * \
                             random.uniform(0.01, 0.05) # Small fraction shifts per year

                shift_amount = max(0, shift_away)
                shifted_walk = split['walk'] * (shift_amount / (split['walk'] + split['rickshaw'])) if (split['walk'] + split['rickshaw']) > 0 else 0
                shifted_rickshaw = split['rickshaw'] * (shift_amount / (split['walk'] + split['rickshaw'])) if (split['walk'] + split['rickshaw']) > 0 else 0

                split['walk'] -= shifted_walk
                split['rickshaw'] -= shifted_rickshaw

                # Shift towards bus and car/taxi (example distribution)
                split['bus'] = split.get('bus', 0) + shift_amount * 0.6
                split['car/taxi'] = split.get('car/taxi', 0) + shift_amount * 0.3
                split['other'] = split.get('other', 0) + shift_amount * 0.1

                # Normalize to 100%
                total_split = sum(split.values())
                if total_split > 0:
                    for mode, value in split.items():
                        split[mode] = (value / total_split) * 100

            # Placeholder: Road density might increase based on investment/governance
            self.road_density[city] *= (1 + random.uniform(0.001, 0.005)) # Very slow increase
            self.public_transit_coverage[city] = min(1.0, self.public_transit_coverage[city]*(1 + random.uniform(0.005, 0.025))) # Slow increase


        print(f"    Dhaka Avg Commute Time Estimate: {self.avg_commute_time.get('Dhaka', 'N/A'):.1f} mins")
        if 'Dhaka' in self.modal_split:
            print(f"    Dhaka Modal Split Estimate (Walk%): {self.modal_split['Dhaka'].get('walk', 'N/A'):.1f}")
        self.current_year = year

    def get_transport_state(self):
        return {
            'modal_split': self.modal_split,
            'avg_commute_time': self.avg_commute_time,
            'road_density': self.road_density,
            'public_transit_coverage': self.public_transit_coverage
        } 
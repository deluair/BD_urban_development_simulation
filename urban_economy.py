import random

class UrbanEconomyModel:
    """Model economic activities and livelihood systems in Bangladesh cities"""
    def __init__(self, config):
        self.gdp_per_capita = config['economy']['gdp_per_capita'].copy()
        self.unemployment = config['economy']['unemployment_rate'].copy()
        self.sectoral_employment = config['economy']['sectoral_employment'].copy()
        self.informal_share = config['economy']['informal_economy_share'].copy()
        self.current_year = 2025
        print("UrbanEconomyModel Initialized")

    def simulate_step(self, year, population_data, infrastructure_data):
        """Simulates economic growth, unemployment shifts, and sectoral changes."""
        print(f"  Simulating Economic Dynamics for year {year}...")

        for city in self.gdp_per_capita:
            # --- GDP Growth ---
            # Factors: Base rate, infrastructure quality (power, internet), population growth (demand)
            base_growth = random.uniform(0.04, 0.07) # National/base growth range

            # Infrastructure multiplier (simplistic average)
            power_factor = infrastructure_data.get('power_reliability', {}).get(city, 0.9) / 0.9
            internet_factor = infrastructure_data.get('internet_penetration', {}).get(city, 0.6) / 0.6
            infra_multiplier = (power_factor + internet_factor) / 2

            growth_factor = 1 + base_growth * infra_multiplier
            self.gdp_per_capita[city] *= growth_factor

            # --- Unemployment ---
            # Factors: GDP growth (inverse), population growth (direct), labor force participation (TBD)
            gdp_growth = growth_factor - 1
            # Placeholder: unemployment decreases with high GDP growth, increases slightly with population pressure
            unemployment_change = - (gdp_growth - 0.05) * 0.1 # Decrease if growth > 5%
            # Add effect of population growth (needs proper labor force calculation later)
            # unemployment_change += (population_growth_rate - 0.03) * 0.05

            self.unemployment[city] *= (1 + unemployment_change + random.uniform(-0.005, 0.005))
            self.unemployment[city] = max(0.02, min(0.15, self.unemployment.get(city, 0.07))) # Bounds

            # --- Sectoral Shift --- (Placeholder)
            # Driven by development stage (GDP), investment, education levels (social)
            # Simple shift towards services as GDP grows
            sectors = self.sectoral_employment.get(city)
            if sectors:
                gdp_level_factor = self.gdp_per_capita[city] / 5000 # Relative to Dhaka start
                shift_to_services = gdp_level_factor * 0.1 * random.uniform(0.01, 0.05)

                transferable_industry = sectors.get('industry', 30) * shift_to_services * 0.6
                transferable_informal = sectors.get('informal', 10) * shift_to_services * 0.4

                sectors['services'] = min(85, sectors.get('services', 50) + transferable_industry + transferable_informal)
                sectors['industry'] = max(5, sectors.get('industry', 30) - transferable_industry)
                sectors['informal'] = max(5, sectors.get('informal', 10) - transferable_informal)

                # Normalize
                total = sum(sectors.values())
                if total > 0:
                    for sector, value in sectors.items():
                        sectors[sector] = (value / total) * 100

            # --- Informal Economy Share --- (Placeholder)
            # Might decrease with formal sector growth, regulation (governance)
            self.informal_share[city] = self.informal_share.get(city, 0.3) * (1 - (gdp_growth - 0.04)*0.05 + random.uniform(-0.005, 0.005))
            self.informal_share[city] = max(0.1, min(0.5, self.informal_share[city]))


        print(f"    Dhaka GDP per Capita Estimate: ${self.gdp_per_capita.get('Dhaka', 'N/A'):.0f}")
        print(f"    Chattogram Unemployment Rate Estimate: {self.unemployment.get('Chattogram', 'N/A'):.3f}")
        self.current_year = year

    def get_economy_state(self):
        return {
            'gdp_per_capita': self.gdp_per_capita,
            'unemployment': self.unemployment,
            'sectoral_employment': self.sectoral_employment,
            'informal_share': self.informal_share
        } 
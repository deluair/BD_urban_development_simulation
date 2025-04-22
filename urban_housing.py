import random

class UrbanHousingModel:
    """Model housing production, markets and affordability in Bangladesh cities"""
    def __init__(self, config):
        self.housing_stock = config['housing']['initial_housing_stock'].copy()
        self.prices = config['housing']['avg_house_price'].copy()
        self.rents = config['housing']['avg_rent'].copy()
        self.affordability = config['housing']['affordability_ratio'].copy()
        self.current_year = 2025
        print("UrbanHousingModel Initialized")

    def simulate_step(self, year, population_data, economy_data):
        """Simulates housing stock changes, price adjustments, and affordability."""
        print(f"  Simulating Housing Dynamics for year {year}...")

        # Calculate housing need based on population and household size
        avg_household_size = 4.5 # Could be city-specific or change over time
        housing_need = {}
        for city, pop in population_data.items():
            housing_need[city] = pop / avg_household_size

        for city, stock in self.housing_stock.items():
            current_supply = stock.get('formal', 0) + stock.get('informal', 0)
            needed = housing_need.get(city, 0)
            deficit = needed - current_supply

            # --- Housing Construction (Placeholder) ---
            # Formal construction might depend on profitability, regulations (governance), land availability (growth model)
            # Informal growth depends on deficit and lack of formal options
            if deficit > 0:
                # Assume only a fraction of the *deficit* is met by new construction this year
                formal_construction_rate = random.uniform(0.02, 0.05) # % of deficit met by formal sector
                informal_construction_rate = random.uniform(0.1, 0.2) # % of deficit met by informal sector

                new_formal = int(deficit * formal_construction_rate)
                new_informal = int(deficit * informal_construction_rate)

                stock['formal'] = stock.get('formal', 0) + new_formal
                stock['informal'] = stock.get('informal', 0) + new_informal
            else:
                 # Optional: Add logic for vacancy or demolition if supply exceeds need
                 pass

            # --- Price/Rent Adjustment (Placeholder) ---
            # Should depend on supply/demand imbalance, economic conditions (GDP growth), construction costs
            demand_pressure = max(0, deficit / current_supply) if current_supply > 0 else 0.1 # Ratio of deficit to supply
            gdp_growth_factor = (economy_data.get('gdp_per_capita', {}).get(city, 5000) / 5000) # Relative GDP factor

            price_increase_rate = random.uniform(0.01, 0.03) + demand_pressure * 0.1 + (gdp_growth_factor -1) * 0.05
            rent_increase_rate = random.uniform(0.01, 0.04) + demand_pressure * 0.15 + (gdp_growth_factor -1) * 0.03

            self.prices[city] = self.prices.get(city, 50) * (1 + price_increase_rate)
            self.rents[city] = self.rents.get(city, 15000) * (1 + rent_increase_rate)

            # --- Affordability Update --- (Price-to-Income Ratio)
            # Requires income data (e.g., from economy model)
            # Placeholder: Link affordability ratio inversely to price changes
            # A proper calculation would use median income vs median house price
            self.affordability[city] = self.affordability.get(city, 15) * (1 + price_increase_rate * 0.5) # Worsens with price increase
            self.affordability[city] = max(5, self.affordability[city]) # Floor value


        print(f"    Dhaka Housing Stock Estimate: Formal={self.housing_stock.get('Dhaka', {}).get('formal', 'N/A')}, Informal={self.housing_stock.get('Dhaka', {}).get('informal', 'N/A')}")
        print(f"    Dhaka Avg House Price (Lakh BDT): {self.prices.get('Dhaka', 'N/A'):.1f}")
        print(f"    Dhaka Affordability Ratio: {self.affordability.get('Dhaka', 'N/A'):.1f}")
        self.current_year = year

    def get_housing_stock(self):
        return self.housing_stock

    def get_prices(self):
        return self.prices

    def get_rents(self):
        return self.rents

    def get_affordability(self):
        return self.affordability 
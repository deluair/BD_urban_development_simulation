import random

class SmartCityModel:
    """Model digital technology application and smart city development in Bangladesh"""
    def __init__(self, config):
        self.digital_literacy = config['smart_city']['digital_literacy'].copy()
        self.adoption_rate = config['smart_city']['smart_service_adoption'].copy()
        self.iot_density = config['smart_city']['iot_sensor_density'].copy()
        self.current_year = 2025
        print("SmartCityModel Initialized")

    def simulate_step(self, year, infrastructure_data, social_data):
        """Simulates the progress of digital literacy, service adoption, and infrastructure rollout."""
        print(f"  Simulating Smart City Dynamics for year {year}...")

        for city in self.digital_literacy: # Assuming keys exist for all tracked metrics
            # --- Digital Literacy ---
            # Factors: Internet penetration (infra), base literacy (social), specific programs (TBD)
            internet_factor = infrastructure_data.get('internet_penetration', {}).get(city, 0.5)
            base_literacy_factor = social_data.get('literacy', {}).get(city, 0.7)
            literacy_improvement = random.uniform(0.008, 0.025) * internet_factor * base_literacy_factor
            self.digital_literacy[city] = min(0.95, self.digital_literacy.get(city, 0.6) * (1 + literacy_improvement))

            # --- Smart Service Adoption ---
            # Factors: Digital literacy, availability of e-gov services (governance - TBD), perceived usefulness
            adoption_improvement = random.uniform(0.015, 0.04) * self.digital_literacy[city] # Driven by digital literacy
            self.adoption_rate[city] = min(0.9, self.adoption_rate.get(city, 0.25) * (1 + adoption_improvement))

            # --- IoT Sensor Density ---
            # Factors: Investment (public/private), strategic initiatives (governance - TBD)
            # Assuming faster, somewhat independent growth initially
            iot_growth = random.uniform(0.08, 0.20)
            self.iot_density[city] = self.iot_density.get(city, 5) * (1 + iot_growth)

        print(f"    Dhaka Smart Service Adoption Estimate: {self.adoption_rate.get('Dhaka', 'N/A'):.2f}")
        print(f"    Chattogram IoT Sensor Density Estimate: {self.iot_density.get('Chattogram', 'N/A'):.1f}")
        self.current_year = year

    def get_smart_city_state(self):
        return {
            'digital_literacy': self.digital_literacy,
            'smart_service_adoption': self.adoption_rate,
            'iot_sensor_density': self.iot_density
        } 
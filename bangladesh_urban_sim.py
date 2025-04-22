import random
import pandas as pd # Using pandas for potentially more structured data later

# --- Synthetic Data Generation ---

def generate_synthetic_config():
    """Generates a configuration dictionary with synthetic data placeholders."""
    config = {
        # --- Urban Growth Data ---
        'urban_growth': {
            'initial_population': {
                'Dhaka': 18_000_000, 'Chattogram': 5_500_000, 'Khulna': 1_500_000,
                'Sylhet': 800_000, 'Rajshahi': 900_000, 'Barishal': 400_000,
                'Rangpur': 350_000, 'Mymensingh': 500_000, 'Narayanganj': 2_000_000,
                "Cox's Bazar": 600_000
            },
            'annual_growth_rate': { # Simplified average annual % growth
                'Dhaka': 0.035, 'Chattogram': 0.030, 'Khulna': 0.020,
                'Sylhet': 0.032, 'Rajshahi': 0.025, 'Barishal': 0.022,
                'Rangpur': 0.028, 'Mymensingh': 0.030, 'Narayanganj': 0.033,
                "Cox's Bazar": 0.045
            },
            'land_use': { # Simplified initial land use %
                'Dhaka': {'residential': 40, 'commercial': 15, 'industrial': 10, 'informal': 15, 'green': 5, 'water': 15},
                'Chattogram': {'residential': 35, 'commercial': 12, 'industrial': 18, 'informal': 10, 'green': 8, 'water': 17},
                # Add other cities...
            },
            'peri_urban_areas': ['Savar', 'Gazipur', 'Keraniganj'], # Examples near Dhaka
        },
        # --- Housing Data ---
        'housing': {
            'initial_housing_stock': { # Units
                 'Dhaka': {'formal': 3_000_000, 'informal': 1_500_000},
                 'Chattogram': {'formal': 800_000, 'informal': 400_000},
                 # Add other cities...
            },
            'avg_house_price': { # BDT Lakh
                'Dhaka': 80, 'Chattogram': 60, # Add other cities...
            },
            'avg_rent': { # BDT / month
                'Dhaka': 20000, 'Chattogram': 12000, # Add other cities...
            },
            'affordability_ratio': { # Price-to-income
                 'Dhaka': 15, 'Chattogram': 12, # Add other cities...
            }
        },
        # --- Infrastructure Data ---
        'infrastructure': {
             'water_coverage': {'Dhaka': 0.85, 'Chattogram': 0.75, 'Khulna': 0.60}, # Piped water access %
             'sanitation_coverage': {'Dhaka': 0.70, 'Chattogram': 0.60, 'Khulna': 0.50}, # Sewerage/FSM %
             'power_reliability': {'Dhaka': 0.95, 'Chattogram': 0.92, 'Khulna': 0.88}, # % Uptime
             'waste_collection': {'Dhaka': 0.75, 'Chattogram': 0.65, 'Khulna': 0.55}, # % Collected
             'internet_penetration': {'Dhaka': 0.80, 'Chattogram': 0.70, 'Khulna': 0.50}, # % Households
        },
        # --- Transport Data ---
        'transport': {
            'modal_split': { # % trips
                'Dhaka': {'walk': 30, 'rickshaw': 25, 'bus': 20, 'car/taxi': 15, 'other': 10},
                'Chattogram': {'walk': 35, 'rickshaw': 30, 'bus': 15, 'car/taxi': 10, 'other': 10},
                 # Add other cities...
            },
            'avg_commute_time': { # Minutes
                'Dhaka': 60, 'Chattogram': 45, # Add other cities...
            },
            'road_density': { # km/sq km
                'Dhaka': 15, 'Chattogram': 12, # Add other cities...
            },
             'public_transit_coverage': { # % population with access
                'Dhaka': 0.60, 'Chattogram': 0.40, # Add other cities... (Excludes Rickshaws for simplicity)
            }
        },
         # --- Economy Data ---
        'economy': {
            'gdp_per_capita': { # USD
                'Dhaka': 5000, 'Chattogram': 4500, 'Khulna': 3000,
            },
            'unemployment_rate': { # %
                'Dhaka': 0.06, 'Chattogram': 0.07, 'Khulna': 0.08,
            },
            'sectoral_employment': { # %
                'Dhaka': {'services': 60, 'industry': 30, 'informal': 10}, # Simplified
                'Chattogram': {'services': 50, 'industry': 40, 'informal': 10},
            },
            'informal_economy_share': { # % of GDP
                'Dhaka': 0.30, 'Chattogram': 0.35,
            }
        },
        # --- Governance Data ---
        'governance': {
            'municipal_own_revenue': { # % of total budget
                'Dhaka': 0.40, 'Chattogram': 0.35, 'Khulna': 0.25,
            },
            'citizen_satisfaction': { # Index 0-1
                 'Dhaka': 0.5, 'Chattogram': 0.55, 'Khulna': 0.6,
            },
            'planning_compliance': { # % development adhering to plan
                'Dhaka': 0.45, 'Chattogram': 0.50,
            }
        },
        # --- Environment Data ---
        'environment': {
            'air_quality_index': { # AQI avg
                'Dhaka': 180, 'Chattogram': 150, 'Khulna': 120,
            },
            'green_space_ratio': { # % land area
                'Dhaka': 0.05, 'Chattogram': 0.08, 'Khulna': 0.10,
            },
             'flood_prone_area': { # % land area
                'Dhaka': 0.25, 'Chattogram': 0.15, 'Khulna': 0.30, 'Barishal': 0.40,
            },
             'waste_recycling_rate': { # %
                'Dhaka': 0.10, 'Chattogram': 0.08,
            }
        },
        # --- Social Data ---
        'social': {
             'literacy_rate': { # %
                 'Dhaka': 0.80, 'Chattogram': 0.75, 'Khulna': 0.70,
             },
             'access_to_healthcare': { # % pop within X km of facility
                 'Dhaka': 0.90, 'Chattogram': 0.85, 'Khulna': 0.75,
             },
             'social_cohesion_index': { # Index 0-1
                 'Dhaka': 0.6, 'Chattogram': 0.65, 'Khulna': 0.7,
             },
              'crime_rate': { # Per 100k pop
                 'Dhaka': 300, 'Chattogram': 250, 'Khulna': 200,
             }
        },
         # --- Urban-Rural Linkage Data ---
        'urban_rural': {
            'remittance_dependency': { # % household income in surrounding rural areas
                 'Sylhet': 0.40, 'Comilla': 0.30,
            },
            'rural_migration_rate': { # Net annual % into major cities
                'Dhaka': 0.015, 'Chattogram': 0.010,
            },
            'commuter_percentage': { # % workforce commuting from peri-urban/rural
                 'Dhaka': 0.15, 'Chattogram': 0.10,
            }
        },
         # --- Service Delivery Data ---
        'service_delivery': { # Focused on social infra
            'school_density': { # Schools per sq km
                 'Dhaka': 5, 'Chattogram': 4,
            },
            'hospital_beds_per_1000': {
                 'Dhaka': 2.0, 'Chattogram': 1.5,
            },
             'public_space_per_capita': { # sq m
                 'Dhaka': 1.0, 'Chattogram': 1.5,
            }
        },
        # --- Smart City Data ---
        'smart_city': {
            'digital_literacy': { # % population
                 'Dhaka': 0.65, 'Chattogram': 0.60,
            },
            'smart_service_adoption': { # % citizens using e-gov services
                 'Dhaka': 0.30, 'Chattogram': 0.25,
            },
            'iot_sensor_density': { # sensors per sq km (conceptual)
                 'Dhaka': 10, 'Chattogram': 5,
            }
        },
        # --- Resilience Data ---
        'resilience': {
            'early_warning_coverage': { # % pop covered
                'Dhaka': 0.7, 'Chattogram': 0.8, 'Khulna': 0.75, 'Barishal': 0.85, # Coastal/riverine focus
            },
            'building_code_compliance': { # % new builds
                'Dhaka': 0.5, 'Chattogram': 0.55,
            },
            'disaster_recovery_speed': { # Avg time (days) to restore basic services
                'Dhaka': 7, 'Chattogram': 5, 'Khulna': 10,
            }
        }
    }
    return config

# --- Core Component Classes ---

class UrbanGrowthModel:
    """Model urban expansion patterns and spatial transformation in Bangladesh"""
    def __init__(self, config):
        self.population = config['urban_growth']['initial_population'].copy()
        self.growth_rate = config['urban_growth']['annual_growth_rate']
        self.land_use = config['urban_growth']['land_use'] # Simplified state
        self.peri_urban = config['urban_growth']['peri_urban_areas']
        self.current_year = 2025
        print("UrbanGrowthModel Initialized")

    def simulate_step(self, year):
        print(f"  Simulating Urban Growth for year {year}...")
        for city, pop in self.population.items():
            rate = self.growth_rate.get(city, 0.02) # Default growth rate if city not specified
            new_pop = pop * (1 + rate)
            # Add stochasticity/complexity later
            self.population[city] = int(new_pop)
            # Placeholder for land use change logic
            # e.g., increase informal settlement area based on pop growth vs formal housing growth
        print(f"    Dhaka Population Estimate: {self.population.get('Dhaka', 'N/A')}")
        self.current_year = year


class UrbanHousingModel:
    """Model housing production, markets and affordability in Bangladesh cities"""
    def __init__(self, config):
        self.housing_stock = config['housing']['initial_housing_stock'].copy()
        self.prices = config['housing']['avg_house_price']
        self.rents = config['housing']['avg_rent']
        self.affordability = config['housing']['affordability_ratio']
        self.current_year = 2025
        print("UrbanHousingModel Initialized")

    def simulate_step(self, year, population_data):
        print(f"  Simulating Housing Dynamics for year {year}...")
        # Placeholder: Increase housing stock slightly, potentially link to population growth
        for city, stock in self.housing_stock.items():
            pop = population_data.get(city, 0)
            # Very basic: add housing proportional to population increase (needs refinement)
            # Assume average household size ~4.5
            pop_increase = pop - (stock['formal'] + stock['informal'])*4.5 # Crude estimate of housing need based on prev year pop
            if pop_increase > 0:
                 needed_units = pop_increase / 4.5
                 # Assume 60% formal, 40% informal growth (highly simplified)
                 stock['formal'] += int(needed_units * 0.6 * 0.1) # Assume only 10% of needed formal is built
                 stock['informal'] += int(needed_units * 0.4 * 0.5) # Assume 50% of needed informal appears

            # Placeholder: Adjust prices/rents slightly (e.g., based on demand)
            self.prices[city] = self.prices.get(city, 50) * (1 + random.uniform(0.02, 0.05))

        print(f"    Dhaka Housing Stock Estimate: Formal={self.housing_stock.get('Dhaka', {}).get('formal', 'N/A')}, Informal={self.housing_stock.get('Dhaka', {}).get('informal', 'N/A')}")
        self.current_year = year


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

    def simulate_step(self, year, population_data):
        print(f"  Simulating Infrastructure Dynamics for year {year}...")
        # Placeholder: Slowly improve coverage/reliability, perhaps faster in larger cities
        for city in self.water_coverage:
            self.water_coverage[city] = min(1.0, self.water_coverage[city] * (1 + random.uniform(0.01, 0.03)))
            self.sanitation_coverage[city] = min(1.0, self.sanitation_coverage.get(city, 0.5) * (1 + random.uniform(0.01, 0.025)))
            self.power_reliability[city] = min(1.0, self.power_reliability.get(city, 0.8) * (1 + random.uniform(0.005, 0.015)))
            self.waste_collection[city] = min(1.0, self.waste_collection.get(city, 0.5) * (1 + random.uniform(0.01, 0.02)))
            self.internet_penetration[city] = min(1.0, self.internet_penetration.get(city, 0.5) * (1 + random.uniform(0.03, 0.06)))
        print(f"    Dhaka Water Coverage Estimate: {self.water_coverage.get('Dhaka', 'N/A'):.2f}")
        self.current_year = year

class UrbanTransportModel:
    """Model transportation systems and mobility patterns in Bangladesh cities"""
    def __init__(self, config):
        self.modal_split = config['transport']['modal_split'].copy()
        self.avg_commute_time = config['transport']['avg_commute_time'].copy()
        self.road_density = config['transport']['road_density'].copy()
        self.public_transit_coverage = config['transport']['public_transit_coverage'].copy()
        self.current_year = 2025
        print("UrbanTransportModel Initialized")

    def simulate_step(self, year, population_data, infrastructure_data):
        print(f"  Simulating Transport Dynamics for year {year}...")
        # Placeholder: Adjust commute time based on population density/road density (inverse relation?)
        # Placeholder: Slightly shift modal split towards public transit/cars if coverage increases
        for city in self.avg_commute_time:
            pop_density_factor = population_data.get(city, 1000000) / 1000000 # Simplistic
            road_factor = self.road_density.get(city, 10)
            self.avg_commute_time[city] *= (1 + random.uniform(0.01, 0.03) * (pop_density_factor / road_factor)) # Increase commute time

            # Shift modal split slightly towards cars/bus if public transit coverage improves
            if self.public_transit_coverage.get(city, 0) > 0.5: # Arbitrary threshold
                 split = self.modal_split.get(city)
                 if split:
                     split['rickshaw'] = max(0, split['rickshaw'] * 0.99)
                     split['bus'] = split.get('bus', 0) * 1.01
                     # Normalize later if needed

        print(f"    Dhaka Avg Commute Time Estimate: {self.avg_commute_time.get('Dhaka', 'N/A'):.1f} mins")
        self.current_year = year


class UrbanEconomyModel:
    """Model economic activities and livelihood systems in Bangladesh cities"""
    def __init__(self, config):
        self.gdp_per_capita = config['economy']['gdp_per_capita'].copy()
        self.unemployment = config['economy']['unemployment_rate'].copy()
        self.sectoral_employment = config['economy']['sectoral_employment'].copy()
        self.informal_share = config['economy']['informal_economy_share'].copy()
        self.current_year = 2025
        print("UrbanEconomyModel Initialized")

    def simulate_step(self, year, population_data):
        print(f"  Simulating Economic Dynamics for year {year}...")
        # Placeholder: Increase GDP per capita, maybe shift employment slightly towards services
        for city in self.gdp_per_capita:
            growth_factor = 1 + random.uniform(0.04, 0.07) # National target range
            self.gdp_per_capita[city] *= growth_factor
            # Placeholder: slight unemployment change
            self.unemployment[city] *= (1 + random.uniform(-0.01, 0.01))
            self.unemployment[city] = max(0.02, min(0.15, self.unemployment[city])) # Bounds

            # Placeholder shift to services
            sectors = self.sectoral_employment.get(city)
            if sectors:
                sectors['services'] = min(80, sectors.get('services', 50) + 0.5)
                sectors['industry'] = max(10, sectors.get('industry', 30) - 0.3)
                sectors['informal'] = max(5, sectors.get('informal', 10) - 0.2) # Simplistic decline

        print(f"    Dhaka GDP per Capita Estimate: ${self.gdp_per_capita.get('Dhaka', 'N/A'):.0f}")
        self.current_year = year


class UrbanGovernanceModel:
    """Model governance frameworks and planning systems for Bangladesh cities"""
    def __init__(self, config):
        self.own_revenue = config['governance']['municipal_own_revenue'].copy()
        self.satisfaction = config['governance']['citizen_satisfaction'].copy()
        self.compliance = config['governance']['planning_compliance'].copy()
        self.current_year = 2025
        print("UrbanGovernanceModel Initialized")

    def simulate_step(self, year, infrastructure_data):
        print(f"  Simulating Governance Dynamics for year {year}...")
        # Placeholder: Slight random changes, maybe link satisfaction to service levels
        for city in self.satisfaction:
             # Link satisfaction to avg service coverage (simplistic)
             avg_coverage = (infrastructure_data['water_coverage'].get(city, 0.5) +
                             infrastructure_data['sanitation_coverage'].get(city, 0.5) +
                             infrastructure_data['power_reliability'].get(city, 0.5) +
                             infrastructure_data['waste_collection'].get(city, 0.5)) / 4
             satisfaction_change = (avg_coverage - 0.6) * 0.1 # Adjust based on deviation from 0.6 baseline
             self.satisfaction[city] = max(0, min(1, self.satisfaction[city] + satisfaction_change + random.uniform(-0.02, 0.02)))

             self.own_revenue[city] *= (1 + random.uniform(0.0, 0.01)) # Slight potential increase
             self.compliance[city] *= (1 + random.uniform(-0.01, 0.01)) # Random fluctuation

        print(f"    Dhaka Citizen Satisfaction Estimate: {self.satisfaction.get('Dhaka', 'N/A'):.2f}")
        self.current_year = year

class UrbanEnvironmentModel:
    """Model environmental systems and sustainability in Bangladesh cities"""
    def __init__(self, config):
        self.aqi = config['environment']['air_quality_index'].copy()
        self.green_space = config['environment']['green_space_ratio'].copy()
        self.flood_prone = config['environment']['flood_prone_area'].copy()
        self.recycling_rate = config['environment']['waste_recycling_rate'].copy()
        self.current_year = 2025
        print("UrbanEnvironmentModel Initialized")

    def simulate_step(self, year, population_data, transport_data):
        print(f"  Simulating Environmental Dynamics for year {year}...")
        # Placeholder: AQI worsens with population/traffic, green space decreases, recycling improves slowly
        for city in self.aqi:
            pop_factor = population_data.get(city, 1000000) / 10000000 # Relative to 10M
            commute_factor = transport_data['avg_commute_time'].get(city, 60) / 60 # Relative to 60 mins
            self.aqi[city] += random.uniform(1, 5) * pop_factor * commute_factor # Worsens AQI

            self.green_space[city] *= (1 - random.uniform(0.001, 0.005)) # Slight decrease
            self.recycling_rate[city] = min(0.5, self.recycling_rate.get(city, 0.1) * (1 + random.uniform(0.01, 0.04)))

        print(f"    Dhaka AQI Estimate: {self.aqi.get('Dhaka', 'N/A'):.0f}")
        self.current_year = year


class UrbanSocialModel:
    """Model social structures, cultural patterns and community dynamics in Bangladesh cities"""
    def __init__(self, config):
        self.literacy = config['social']['literacy_rate'].copy()
        self.healthcare_access = config['social']['access_to_healthcare'].copy()
        self.cohesion = config['social']['social_cohesion_index'].copy()
        self.crime_rate = config['social']['crime_rate'].copy()
        self.current_year = 2025
        print("UrbanSocialModel Initialized")

    def simulate_step(self, year, population_data, economy_data, governance_data):
        print(f"  Simulating Social Dynamics for year {year}...")
        # Placeholder: Literacy improves, healthcare access improves, crime fluctuates (e.g., with unemployment)
        for city in self.literacy:
            self.literacy[city] = min(1.0, self.literacy[city] * (1 + random.uniform(0.005, 0.01)))
            self.healthcare_access[city] = min(1.0, self.healthcare_access[city] * (1 + random.uniform(0.005, 0.015)))

            # Link crime to unemployment and cohesion inversely
            unemployment_factor = economy_data['unemployment'].get(city, 0.07) / 0.07 # Relative to 7%
            cohesion_factor = (1 - self.cohesion.get(city, 0.6)) / 0.4 # Inverse, relative to 0.6
            self.crime_rate[city] *= (1 + random.uniform(-0.02, 0.02) + 0.01 * unemployment_factor + 0.01 * cohesion_factor)
            self.crime_rate[city] = max(50, self.crime_rate[city])

            # Link cohesion to satisfaction
            satisfaction_factor = governance_data['satisfaction'].get(city, 0.5)
            self.cohesion[city] = max(0, min(1, self.cohesion[city] + (satisfaction_factor - 0.5)*0.05 + random.uniform(-0.01, 0.01)))

        print(f"    Dhaka Literacy Rate Estimate: {self.literacy.get('Dhaka', 'N/A'):.2f}")
        self.current_year = year


class UrbanRuralLinkageModel:
    """Model interconnections between urban centers and rural hinterlands in Bangladesh"""
    def __init__(self, config):
        self.remittance_dep = config['urban_rural']['remittance_dependency'].copy()
        self.migration_rate = config['urban_rural']['rural_migration_rate'].copy() # Net rate into city
        self.commuter_perc = config['urban_rural']['commuter_percentage'].copy()
        self.current_year = 2025
        print("UrbanRuralLinkageModel Initialized")

    def simulate_step(self, year, economy_data, transport_data):
        print(f"  Simulating Urban-Rural Linkages for year {year}...")
        # Placeholder: Migration rate might decrease slightly if urban unemployment rises
        # Placeholder: Commuting might increase if transport improves relative to housing cost
        for city in self.migration_rate:
             unemployment_factor = economy_data['unemployment'].get(city, 0.07)
             # Reduce migration slightly if unemployment is high
             self.migration_rate[city] *= (1 - (unemployment_factor - 0.06)*0.1 + random.uniform(-0.005, 0.005))
             self.migration_rate[city] = max(0, self.migration_rate[city]) # Cannot be negative net inflow here

        # Simplistic: Increase commuting if commute time decreases (relative?)
        for city in self.commuter_perc:
            commute_time = transport_data['avg_commute_time'].get(city, 60)
            if commute_time < 55: # Arbitrary threshold for 'improvement'
                self.commuter_perc[city] *= (1 + random.uniform(0, 0.01))
            else:
                 self.commuter_perc[city] *= (1 + random.uniform(-0.005, 0.005)) # Fluctuate otherwise

        print(f"    Dhaka Net Rural Migration Rate Estimate: {self.migration_rate.get('Dhaka', 'N/A'):.3f}")
        self.current_year = year


class UrbanServiceModel: # Focused on Social Infrastructure Delivery
    """Model public service provision and social infrastructure in Bangladesh cities"""
    def __init__(self, config):
        self.school_density = config['service_delivery']['school_density'].copy()
        self.hospital_beds = config['service_delivery']['hospital_beds_per_1000'].copy()
        self.public_space = config['service_delivery']['public_space_per_capita'].copy()
        self.current_year = 2025
        print("UrbanServiceModel Initialized")

    def simulate_step(self, year, population_data, governance_data):
        print(f"  Simulating Urban Service (Social Infra) Dynamics for year {year}...")
        # Placeholder: Increase service density/availability slowly, maybe link to municipal revenue
        for city in self.school_density:
            revenue_factor = governance_data['own_revenue'].get(city, 0.3) / 0.3 # Relative to 30%
            pop_factor = population_data.get(city, 1000000) / 10000000 # Relative pop size

            self.school_density[city] *= (1 + random.uniform(0.001, 0.005) * revenue_factor)
            self.hospital_beds[city] *= (1 + random.uniform(0.002, 0.008) * revenue_factor)
            # Public space per capita likely decreases with population unless proactive measures taken
            self.public_space[city] /= (1 + population_data.get(city, 1) / 1000000 * 0.01) # Decrease slightly with pop growth
            self.public_space[city] *= (1 + random.uniform(0.0, 0.003)*revenue_factor) # Small potential increase effort

        print(f"    Dhaka Hospital Beds per 1000 Estimate: {self.hospital_beds.get('Dhaka', 'N/A'):.2f}")
        self.current_year = year


class SmartCityModel:
    """Model digital technology application and smart city development in Bangladesh"""
    def __init__(self, config):
        self.digital_literacy = config['smart_city']['digital_literacy'].copy()
        self.adoption_rate = config['smart_city']['smart_service_adoption'].copy()
        self.iot_density = config['smart_city']['iot_sensor_density'].copy()
        self.current_year = 2025
        print("SmartCityModel Initialized")

    def simulate_step(self, year, infrastructure_data, social_data):
        print(f"  Simulating Smart City Dynamics for year {year}...")
        # Placeholder: Increase literacy and adoption, link to internet penetration and education levels
        for city in self.digital_literacy:
            internet_factor = infrastructure_data['internet_penetration'].get(city, 0.5)
            literacy_factor = social_data['literacy'].get(city, 0.7)

            self.digital_literacy[city] = min(1.0, self.digital_literacy[city] * (1 + random.uniform(0.01, 0.03) * internet_factor * literacy_factor))
            self.adoption_rate[city] = min(1.0, self.adoption_rate[city] * (1 + random.uniform(0.02, 0.05) * self.digital_literacy[city]))
            self.iot_density[city] *= (1 + random.uniform(0.05, 0.15)) # Assume faster growth for sensors

        print(f"    Dhaka Smart Service Adoption Estimate: {self.adoption_rate.get('Dhaka', 'N/A'):.2f}")
        self.current_year = year

class UrbanResilienceModel:
    """Model risk reduction and resilience building in Bangladesh cities"""
    def __init__(self, config):
        self.warning_coverage = config['resilience']['early_warning_coverage'].copy()
        self.code_compliance = config['resilience']['building_code_compliance'].copy()
        self.recovery_speed = config['resilience']['disaster_recovery_speed'].copy() # Lower is better
        self.current_year = 2025
        print("UrbanResilienceModel Initialized")

    def simulate_step(self, year, governance_data, environment_data):
        print(f"  Simulating Urban Resilience Dynamics for year {year}...")
        # Placeholder: Improve warning coverage, compliance improves slightly, recovery speed improves slightly (decreases)
        for city in self.warning_coverage:
             compliance_factor = governance_data['compliance'].get(city, 0.5) # Planning compliance link

             self.warning_coverage[city] = min(1.0, self.warning_coverage[city] * (1 + random.uniform(0.01, 0.04)))
             self.code_compliance[city] = min(1.0, self.code_compliance.get(city, 0.5) * (1 + random.uniform(0.005, 0.02) * compliance_factor))
             # Recovery speed improves (time decreases) slightly
             self.recovery_speed[city] = max(1, self.recovery_speed.get(city, 10) * (1 - random.uniform(0.01, 0.03)))

        print(f"    Chattogram Building Code Compliance Estimate: {self.code_compliance.get('Chattogram', 'N/A'):.2f}")
        self.current_year = year


# --- Data Handler ---

class UrbanDataHandler:
    """Handle urban development data loading and preprocessing"""
    def __init__(self):
        self.config = generate_synthetic_config()
        print("UrbanDataHandler Initialized with synthetic config.")

    def get_config(self):
        return self.config

    def load_historical_data(self, sources):
        # Placeholder for loading real data
        print(f"Placeholder: Would load historical data from {sources}")
        # Potentially update self.config here
        pass

    def integrate_realtime_data(self, api_connections):
        # Placeholder for integrating real-time data
        print(f"Placeholder: Would connect to real-time data APIs: {api_connections}")
        # Potentially update self.config or internal state periodically
        pass

# --- Analysis Engine ---

class UrbanAnalysisEngine:
    """Analyze and visualize urban simulation results"""
    def __init__(self, simulation_instance):
        self.sim = simulation_instance
        print("UrbanAnalysisEngine Initialized")

    def generate_urban_performance_metrics(self, year):
        print(f"
--- Performance Metrics for Year {year} ---")
        # Example metrics - pull data from the simulation models
        dhaka_pop = self.sim.urban_growth.population.get('Dhaka', 'N/A')
        dhaka_affordability = self.sim.urban_housing.affordability.get('Dhaka', 'N/A')
        dhaka_aqi = self.sim.urban_environment.aqi.get('Dhaka', 'N/A')
        chattogram_transit_cov = self.sim.urban_transport.public_transit_coverage.get('Chattogram', 'N/A')
        khulna_sanitation = self.sim.urban_infrastructure.sanitation_coverage.get('Khulna', 'N/A')

        print(f"Dhaka Population: {dhaka_pop}")
        print(f"Dhaka Housing Affordability Ratio: {dhaka_affordability:.1f}")
        print(f"Dhaka AQI: {dhaka_aqi:.0f}")
        print(f"Chattogram Public Transit Coverage: {chattogram_transit_cov:.2f}")
        print(f"Khulna Sanitation Coverage: {khulna_sanitation:.2f}")
        # Add many more relevant KPIs

    def analyze_urbanization_dynamics(self):
        print("
--- Analyzing Urbanization Dynamics (Summary) ---")
        # Example analysis: Compare growth rates or changes over time
        initial_pop = self.sim.initial_config['urban_growth']['initial_population']
        current_pop = self.sim.urban_growth.population
        for city in current_pop:
            if city in initial_pop:
                 growth = ((current_pop[city] / initial_pop[city]) - 1) * 100
                 print(f"{city}: Population growth = {growth:.1f}% over {self.sim.current_year - 2025} years")
        # Add analysis of spatial changes, inequality, etc.


# --- Main Simulation Environment ---

class BangladeshUrbanDevelopmentSimulation:
    """Main simulation environment integrating all components"""
    def __init__(self, config):
        self.initial_config = config # Keep initial state for comparison
        self.urban_growth = UrbanGrowthModel(config)
        self.urban_housing = UrbanHousingModel(config)
        self.urban_infrastructure = UrbanInfrastructureModel(config)
        self.urban_transport = UrbanTransportModel(config)
        self.urban_economy = UrbanEconomyModel(config)
        self.urban_governance = UrbanGovernanceModel(config)
        self.urban_environment = UrbanEnvironmentModel(config)
        self.urban_social = UrbanSocialModel(config)
        self.urban_rural_linkage = UrbanRuralLinkageModel(config)
        self.urban_service = UrbanServiceModel(config)
        self.smart_city = SmartCityModel(config)
        self.urban_resilience = UrbanResilienceModel(config)
        self.current_year = 2025
        print("
BangladeshUrbanDevelopmentSimulation Initialized
" + "="*40)

    def run_simulation(self, years=10, scenarios=None):
        """Execute simulation for the specified number of years."""
        print(f"Starting Simulation Run: {years} years (2025-{2025 + years -1})")
        if scenarios:
            print(f"Applying Scenarios: {scenarios}") # Placeholder for scenario logic

        start_year = 2025
        end_year = start_year + years

        for year in range(start_year, end_year):
            print(f"
--- Simulating Year {year} ---")

            # Store state potentially needed by other models this step
            current_population = self.urban_growth.population
            current_infrastructure_state = {
                'water_coverage': self.urban_infrastructure.water_coverage,
                'sanitation_coverage': self.urban_infrastructure.sanitation_coverage,
                'power_reliability': self.urban_infrastructure.power_reliability,
                'waste_collection': self.urban_infrastructure.waste_collection,
                'internet_penetration': self.urban_infrastructure.internet_penetration,
            }
            current_transport_state = {
                 'avg_commute_time': self.urban_transport.avg_commute_time,
                 'road_density': self.urban_transport.road_density,
            }
            current_economy_state = {
                 'unemployment': self.urban_economy.unemployment,
            }
            current_governance_state = {
                 'satisfaction': self.urban_governance.satisfaction,
                 'own_revenue': self.urban_governance.own_revenue,
                 'compliance': self.urban_governance.compliance,
            }
             current_social_state = {
                 'literacy': self.urban_social.literacy,
            }
            current_environment_state = {
                # Add relevant state if needed by other models
            }


            # Run simulation steps for each component model
            # Pass necessary data between models (this is a simplified dependency chain)
            self.urban_growth.simulate_step(year)
            self.urban_housing.simulate_step(year, self.urban_growth.population)
            self.urban_infrastructure.simulate_step(year, self.urban_growth.population)
            self.urban_transport.simulate_step(year, self.urban_growth.population, current_infrastructure_state)
            self.urban_economy.simulate_step(year, self.urban_growth.population)
            self.urban_governance.simulate_step(year, current_infrastructure_state)
            self.urban_environment.simulate_step(year, self.urban_growth.population, current_transport_state)
            self.urban_social.simulate_step(year, self.urban_growth.population, current_economy_state, current_governance_state)
            self.urban_rural_linkage.simulate_step(year, current_economy_state, current_transport_state)
            self.urban_service.simulate_step(year, self.urban_growth.population, current_governance_state)
            self.smart_city.simulate_step(year, current_infrastructure_state, current_social_state)
            self.urban_resilience.simulate_step(year, current_governance_state, current_environment_state) # Pass relevant state

            self.current_year = year

        print("
" + "="*40 + "
Simulation Run Complete.")


# --- Main Execution ---
if __name__ == "__main__":
    # 1. Initialize Data Handler (loads synthetic config)
    data_handler = UrbanDataHandler()
    config = data_handler.get_config()

    # 2. Initialize Main Simulation Environment
    simulation = BangladeshUrbanDevelopmentSimulation(config)

    # 3. Initialize Analysis Engine
    analysis_engine = UrbanAnalysisEngine(simulation)

    # 4. Run the Simulation
    simulation.run_simulation(years=10) # Simulate 2025-2034

    # 5. Analyze Results (Example)
    analysis_engine.generate_urban_performance_metrics(simulation.current_year)
    analysis_engine.analyze_urbanization_dynamics()

    # Example: Access final state of a specific model
    print("
--- Final State Example ---")
    print("Final Dhaka Population:", simulation.urban_growth.population.get('Dhaka'))
    print("Final Dhaka Housing Stock:", simulation.urban_housing.housing_stock.get('Dhaka'))
    print("Final Dhaka AQI:", simulation.urban_environment.aqi.get('Dhaka'))


</rewritten_file>
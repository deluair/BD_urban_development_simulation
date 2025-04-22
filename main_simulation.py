import random
import pandas as pd
import matplotlib.pyplot as plt
import os

# Import model components from their respective files
from urban_growth import UrbanGrowthModel
from urban_housing import UrbanHousingModel
from urban_infrastructure import UrbanInfrastructureModel
from urban_transport import UrbanTransportModel
from urban_economy import UrbanEconomyModel
from urban_governance import UrbanGovernanceModel
from urban_environment import UrbanEnvironmentModel
from urban_social import UrbanSocialModel
from urban_rural_linkage import UrbanRuralLinkageModel
from urban_service import UrbanServiceModel
from smart_city import SmartCityModel
from urban_resilience import UrbanResilienceModel

# --- Synthetic Data Generation (copied from original for self-containment) ---
def generate_synthetic_config():
    """Generates a configuration dictionary with synthetic data placeholders."""
    config = {
        # ... (Keep the full config dictionary structure as defined before)
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
                'Khulna': {'residential': 45, 'commercial': 10, 'industrial': 15, 'informal': 8, 'green': 10, 'water': 12},
            },
            'peri_urban_areas': ['Savar', 'Gazipur', 'Keraniganj'],
        },
        'housing': {
            'initial_housing_stock': {
                 'Dhaka': {'formal': 3_000_000, 'informal': 1_500_000},
                 'Chattogram': {'formal': 800_000, 'informal': 400_000},
                 'Khulna': {'formal': 250_000, 'informal': 100_000},
            },
            'avg_house_price': {'Dhaka': 80, 'Chattogram': 60, 'Khulna': 40},
            'avg_rent': {'Dhaka': 20000, 'Chattogram': 12000, 'Khulna': 8000},
            'affordability_ratio': {'Dhaka': 15, 'Chattogram': 12, 'Khulna': 10}
        },
        'infrastructure': {
             'water_coverage': {'Dhaka': 0.85, 'Chattogram': 0.75, 'Khulna': 0.60},
             'sanitation_coverage': {'Dhaka': 0.70, 'Chattogram': 0.60, 'Khulna': 0.50},
             'power_reliability': {'Dhaka': 0.95, 'Chattogram': 0.92, 'Khulna': 0.88},
             'waste_collection': {'Dhaka': 0.75, 'Chattogram': 0.65, 'Khulna': 0.55},
             'internet_penetration': {'Dhaka': 0.80, 'Chattogram': 0.70, 'Khulna': 0.50},
        },
        'transport': {
            'modal_split': {
                'Dhaka': {'walk': 30, 'rickshaw': 25, 'bus': 20, 'car/taxi': 15, 'other': 10},
                'Chattogram': {'walk': 35, 'rickshaw': 30, 'bus': 15, 'car/taxi': 10, 'other': 10},
                'Khulna': {'walk': 40, 'rickshaw': 35, 'bus': 10, 'car/taxi': 5, 'other': 10},
            },
            'avg_commute_time': {'Dhaka': 60, 'Chattogram': 45, 'Khulna': 35},
            'road_density': {'Dhaka': 15, 'Chattogram': 12, 'Khulna': 10},
             'public_transit_coverage': {'Dhaka': 0.60, 'Chattogram': 0.40, 'Khulna': 0.30}
        },
        'economy': {
            'gdp_per_capita': {'Dhaka': 5000, 'Chattogram': 4500, 'Khulna': 3000},
            'unemployment_rate': {'Dhaka': 0.06, 'Chattogram': 0.07, 'Khulna': 0.08},
            'sectoral_employment': {
                'Dhaka': {'services': 60, 'industry': 30, 'informal': 10},
                'Chattogram': {'services': 50, 'industry': 40, 'informal': 10},
                 'Khulna': {'services': 55, 'industry': 35, 'informal': 10},
            },
            'informal_economy_share': {'Dhaka': 0.30, 'Chattogram': 0.35, 'Khulna': 0.40}
        },
        'governance': {
            'municipal_own_revenue': {'Dhaka': 0.40, 'Chattogram': 0.35, 'Khulna': 0.25},
            'citizen_satisfaction': {'Dhaka': 0.5, 'Chattogram': 0.55, 'Khulna': 0.6},
            'planning_compliance': {'Dhaka': 0.45, 'Chattogram': 0.50, 'Khulna': 0.55}
        },
        'environment': {
            'air_quality_index': {'Dhaka': 180, 'Chattogram': 150, 'Khulna': 120},
            'green_space_ratio': {'Dhaka': 0.05, 'Chattogram': 0.08, 'Khulna': 0.10},
             'flood_prone_area': {'Dhaka': 0.25, 'Chattogram': 0.15, 'Khulna': 0.30, 'Barishal': 0.40},
             'waste_recycling_rate': {'Dhaka': 0.10, 'Chattogram': 0.08, 'Khulna': 0.05}
        },
        'social': {
             'literacy_rate': {'Dhaka': 0.80, 'Chattogram': 0.75, 'Khulna': 0.70},
             'access_to_healthcare': {'Dhaka': 0.90, 'Chattogram': 0.85, 'Khulna': 0.75},
             'social_cohesion_index': {'Dhaka': 0.6, 'Chattogram': 0.65, 'Khulna': 0.7},
              'crime_rate': {'Dhaka': 300, 'Chattogram': 250, 'Khulna': 200}
        },
        'urban_rural': {
            'remittance_dependency': {'Sylhet': 0.40, 'Comilla': 0.30},
            'rural_migration_rate': {'Dhaka': 0.015, 'Chattogram': 0.010, 'Khulna': 0.008},
            'commuter_percentage': {'Dhaka': 0.15, 'Chattogram': 0.10, 'Khulna': 0.08}
        },
        'service_delivery': {
            'school_density': {'Dhaka': 5, 'Chattogram': 4, 'Khulna': 3},
            'hospital_beds_per_1000': {'Dhaka': 2.0, 'Chattogram': 1.5, 'Khulna': 1.2},
             'public_space_per_capita': {'Dhaka': 1.0, 'Chattogram': 1.5, 'Khulna': 1.8}
        },
        'smart_city': {
            'digital_literacy': {'Dhaka': 0.65, 'Chattogram': 0.60, 'Khulna': 0.50},
            'smart_service_adoption': {'Dhaka': 0.30, 'Chattogram': 0.25, 'Khulna': 0.15},
            'iot_sensor_density': {'Dhaka': 10, 'Chattogram': 5, 'Khulna': 2}
        },
        'resilience': {
            'early_warning_coverage': {'Dhaka': 0.7, 'Chattogram': 0.8, 'Khulna': 0.75, 'Barishal': 0.85},
            'building_code_compliance': {'Dhaka': 0.5, 'Chattogram': 0.55, 'Khulna': 0.6},
            'disaster_recovery_speed': {'Dhaka': 7, 'Chattogram': 5, 'Khulna': 10}
        }
    }
    return config

# --- Data Handler ---
class UrbanDataHandler:
    """Handle urban development data loading and preprocessing"""
    def __init__(self):
        self.config = generate_synthetic_config()
        print("UrbanDataHandler Initialized with synthetic config.")

    def get_config(self):
        return self.config

    def load_historical_data(self, sources):
        print(f"Placeholder: Would load historical data from {sources}")
        pass

    def integrate_realtime_data(self, api_connections):
        print(f"Placeholder: Would connect to real-time data APIs: {api_connections}")
        pass

# --- Analysis Engine ---
class UrbanAnalysisEngine:
    """Analyze and visualize urban simulation results"""
    def __init__(self, simulation_instance):
        self.sim = simulation_instance
        self.results = {} # Store results over time
        self.output_dir = "simulation_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"UrbanAnalysisEngine Initialized. Outputs will be saved to '{self.output_dir}'")

    def record_state(self, year):
        """Records the state of key indicators for the given year."""
        state = {
            'population': self.sim.urban_growth.get_population(),
            'land_use': self.sim.urban_growth.get_land_use(),
            'housing_stock': self.sim.urban_housing.get_housing_stock(),
            'avg_house_price': self.sim.urban_housing.get_prices(),
            'affordability_ratio': self.sim.urban_housing.get_affordability(),
            'water_coverage': self.sim.urban_infrastructure.get_infrastructure_state()['water_coverage'],
            'sanitation_coverage': self.sim.urban_infrastructure.get_infrastructure_state()['sanitation_coverage'],
            'power_reliability': self.sim.urban_infrastructure.get_infrastructure_state()['power_reliability'],
            'avg_commute_time': self.sim.urban_transport.get_transport_state()['avg_commute_time'],
            'gdp_per_capita': self.sim.urban_economy.get_economy_state()['gdp_per_capita'],
            'unemployment_rate': self.sim.urban_economy.get_economy_state()['unemployment'],
            'citizen_satisfaction': self.sim.urban_governance.get_governance_state()['citizen_satisfaction'],
            'aqi': self.sim.urban_environment.get_environment_state()['aqi'],
            'green_space': self.sim.urban_environment.get_environment_state()['green_space'],
            'crime_rate': self.sim.urban_social.get_social_state()['crime_rate'],
            'migration_rate': self.sim.urban_rural_linkage.get_linkage_state()['migration_rate'],
            'commuter_percentage': self.sim.urban_rural_linkage.get_linkage_state()['commuter_percentage'],
            'hospital_beds_per_1000': self.sim.urban_service.get_service_state()['hospital_beds_per_1000'],
            'digital_literacy': self.sim.smart_city.get_smart_city_state()['digital_literacy'],
            'building_code_compliance': self.sim.urban_resilience.get_resilience_state()['building_code_compliance'],
            'recovery_speed': self.sim.urban_resilience.get_resilience_state()['disaster_recovery_speed'],
        }
        self.results[year] = state

    def generate_plots(self):
        """Generates plots for key indicators over time."""
        print("\nGenerating plots...")
        if not self.results:
            print("No results to plot.")
            return

        years = sorted(self.results.keys())
        cities = list(self.results[years[0]]['population'].keys()) # Get city list from first year

        # Example Plots (add more as needed)
        plt.figure(figsize=(12, 8))

        # --- Population Plot ---
        plt.subplot(2, 2, 1)
        for city in cities:
            pop_trend = [self.results[y]['population'].get(city, 0) for y in years]
            plt.plot(years, pop_trend, marker='o', linestyle='-', label=city)
        plt.title('Population Growth (2025-{})'.format(years[-1]))
        plt.xlabel('Year')
        plt.ylabel('Population')
        plt.legend(fontsize='small')
        plt.grid(True)

        # --- AQI Plot ---
        plt.subplot(2, 2, 2)
        for city in cities:
             if city in self.results[years[0]]['aqi']: # Check if city has AQI data
                aqi_trend = [self.results[y]['aqi'].get(city, 0) for y in years]
                plt.plot(years, aqi_trend, marker='o', linestyle='-', label=city)
        plt.title('Air Quality Index (AQI)')
        plt.xlabel('Year')
        plt.ylabel('AQI (Higher=Worse)')
        plt.legend(fontsize='small')
        plt.grid(True)

        # --- Affordability Plot ---
        plt.subplot(2, 2, 3)
        for city in cities:
             if city in self.results[years[0]]['affordability_ratio']: # Check if city has data
                aff_trend = [self.results[y]['affordability_ratio'].get(city, 0) for y in years]
                plt.plot(years, aff_trend, marker='o', linestyle='-', label=city)
        plt.title('Housing Affordability Ratio')
        plt.xlabel('Year')
        plt.ylabel('Price-to-Income Ratio')
        plt.legend(fontsize='small')
        plt.grid(True)

        # --- Citizen Satisfaction Plot ---
        plt.subplot(2, 2, 4)
        for city in cities:
            if city in self.results[years[0]]['citizen_satisfaction']: # Check if city has data
                sat_trend = [self.results[y]['citizen_satisfaction'].get(city, 0) for y in years]
                plt.plot(years, sat_trend, marker='o', linestyle='-', label=city)
        plt.title('Citizen Satisfaction Index')
        plt.xlabel('Year')
        plt.ylabel('Satisfaction (0-1)')
        plt.legend(fontsize='small')
        plt.grid(True)


        plt.tight_layout()
        plot_filename = os.path.join(self.output_dir, "key_indicators_plot.png")
        plt.savefig(plot_filename)
        print(f"Plots saved to {plot_filename}")
        # plt.show() # Optionally display plots interactively
        plt.close()

    def generate_html_report(self):
        """Generates an enhanced HTML report summarizing the simulation results."""
        print("Generating enhanced HTML report...")
        if not self.results:
            print("No results to generate report.")
            return

        start_year = min(self.results.keys())
        final_year = max(self.results.keys())
        initial_state = self.results[start_year]
        final_state = self.results[final_year]
        report_filename = os.path.join(self.output_dir, "simulation_report.html")

        # --- Enhanced CSS --- (Added more styles)
        html_css = f"""
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                line-height: 1.6;
                background-color: #f9f9f9;
                color: #333;
            }}
            .container {{ 
                max-width: 1000px; 
                margin: auto; 
                background-color: #fff; 
                padding: 30px; 
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 8px;
            }}
            h1, h2, h3 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px;}}
            h1 {{ text-align: center; }}
            table {{ 
                border-collapse: collapse; 
                width: 100%; 
                margin-bottom: 25px; 
                font-size: 0.9em;
            }}
            th, td {{ 
                border: 1px solid #ddd; 
                padding: 10px; 
                text-align: left; 
            }}
            th {{ 
                background-color: #3498db; 
                color: white;
                text-align: center;
            }}
            tr:nth-child(even) {{ background-color: #f2f9fc; }}
            tr:hover {{ background-color: #eaf4fb; }}
            img {{ 
                max-width: 100%; 
                height: auto; 
                margin-top: 20px; 
                display: block; 
                margin-left: auto; 
                margin-right: auto; 
                border: 1px solid #ddd;
                padding: 5px;
                background-color: #fff;
            }}
            .summary-table td:nth-child(n+3) {{ text-align: right; }} /* Align numbers right */
            .percentage-positive {{ color: green; }}
            .percentage-negative {{ color: red; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 0.8em; color: #777; }}
        </style>
        """

        # --- HTML Header --- 
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Bangladesh Urban Simulation Report ({start_year}-{final_year})</title>
            {html_css}
        </head>
        <body>
            <div class="container">
            <h1>Bangladesh Urban Development Simulation Report</h1>
            <p>This report summarizes the key outcomes of the urban development simulation for selected cities in Bangladesh, running from {start_year} to {final_year}.</p>
            
            <h2>Final State Summary (Year {final_year}) vs Initial State ({start_year})</h2>
        """

        # --- Enhanced Summary Table --- 
        html_content += "<h3>Key Indicators by City</h3>"

        indicators_to_report = { # Use a dict for display name and formatting hints
            'population': {'name': 'Population', 'format': ',.0f'},
            'gdp_per_capita': {'name': 'GDP per Capita (USD)', 'format': ',.0f'},
            'avg_commute_time': {'name': 'Avg Commute Time (min)', 'format': '.1f'},
            'aqi': {'name': 'Air Quality Index (AQI)', 'format': '.0f', 'higher_is_worse': True},
            'affordability_ratio': {'name': 'Housing Affordability Ratio', 'format': '.1f', 'higher_is_worse': True},
            'water_coverage': {'name': 'Water Coverage (%)', 'format': '.1%'},
            'sanitation_coverage': {'name': 'Sanitation Coverage (%)', 'format': '.1%'},
            'power_reliability': {'name': 'Power Reliability (%)', 'format': '.1%'},
            'citizen_satisfaction': {'name': 'Citizen Satisfaction Index', 'format': '.2f'},
            'unemployment_rate': {'name': 'Unemployment Rate (%)', 'format': '.1%', 'higher_is_worse': True},
            'crime_rate': {'name': 'Crime Rate (per 100k)', 'format': ',.0f', 'higher_is_worse': True},
            'green_space': {'name': 'Green Space (% Area)', 'format': '.1%'},
            'digital_literacy': {'name': 'Digital Literacy (%)', 'format': '.1%'},
            'building_code_compliance': {'name': 'Building Code Compliance (%)', 'format': '.1%'},
            'recovery_speed': {'name': 'Disaster Recovery (Days)', 'format': '.1f', 'higher_is_worse': True},
        }
        
        # Ensure cities are only those present in the final population state
        cities = sorted([city for city in final_state.get('population', {}).keys()])
        
        if not cities:
             html_content += "<p>No city data available for reporting.</p>"
        else:
            report_data = []
            valid_cities_for_report = set(cities) # Start with all cities with population data

            # Pre-filter: Check which cities have *any* data for the required indicators initially and finally
            for indicator_key in indicators_to_report.keys():
                initial_keys = set(initial_state.get(indicator_key, {}).keys())
                final_keys = set(final_state.get(indicator_key, {}).keys())
                valid_cities_for_report &= initial_keys
                valid_cities_for_report &= final_keys
            
            valid_cities_list = sorted(list(valid_cities_for_report))
            
            if not valid_cities_list:
                 html_content += "<p>No cities found with complete data for all reported indicators.</p>"
            else:
                print(f"Generating report table for cities: {valid_cities_list}")
                # --- Build DataFrame directly in wide format --- 
                table_data = {}
                index_order = [] # To maintain indicator order

                for indicator_key, props in indicators_to_report.items():
                    indicator_name = props['name']
                    index_order.append(indicator_name)
                    fmt = props.get('format', '.2f')
                    higher_is_worse = props.get('higher_is_worse', False)
                    table_data[indicator_name] = {}

                    for city in valid_cities_list:
                        initial_val = initial_state.get(indicator_key, {}).get(city)
                        final_val = final_state.get(indicator_key, {}).get(city)
                        
                        initial_col = f"{city} Initial ({start_year})"
                        final_col = f"{city} Final ({final_year})"
                        change_col = f"{city} % Change"

                        initial_val_str = "N/A"
                        final_val_str = "N/A"
                        change_str = "N/A"
                        change_class = ""

                        if initial_val is not None and final_val is not None and isinstance(initial_val, (int, float)) and isinstance(final_val, (int, float)):
                            try:
                                initial_val_str = format(initial_val, fmt)
                                final_val_str = format(final_val, fmt)
                                if initial_val != 0:
                                    change = ((final_val / initial_val) - 1)
                                    change_str = format(change, '.1%')
                                    if change > 0:
                                        change_class = "percentage-positive" if not higher_is_worse else "percentage-negative"
                                    elif change < 0:
                                        change_class = "percentage-negative" if not higher_is_worse else "percentage-positive"
                                else:
                                    change_str = "Inf" if final_val > 0 else "0.0%" 
                            except (ValueError, TypeError):
                                initial_val_str = str(initial_val); final_val_str = str(final_val); change_str = "Calc Error"
                        elif initial_val is not None: initial_val_str = str(initial_val)
                        elif final_val is not None: final_val_str = str(final_val)

                        table_data[indicator_name][initial_col] = initial_val_str
                        table_data[indicator_name][final_col] = final_val_str
                        table_data[indicator_name][change_col] = f'<span class="{change_class}">{change_str}</span>' if change_class else change_str
                
                try:
                    # Create DataFrame from the nested dict structure
                    df_final = pd.DataFrame.from_dict(table_data, orient='index')
                    # Ensure columns are ordered correctly: Initial, Final, Change for each city
                    col_order = []
                    for city in valid_cities_list:
                        col_order.extend([f"{city} Initial ({start_year})", f"{city} Final ({final_year})", f"{city} % Change"])
                    # Reindex to ensure correct column order and handle potentially missing columns gracefully
                    df_final = df_final.reindex(columns=col_order, fill_value="N/A")
                    # Reindex rows to maintain the desired indicator order
                    df_final = df_final.reindex(index=index_order)
                    
                    html_content += df_final.to_html(escape=False, classes='summary-table', border=0, na_rep='N/A')
                except Exception as e:
                    print(f"Error creating final DataFrame for HTML report: {e}")
                    html_content += "<p>Error generating summary table.</p>"

        # --- Plot Section --- 
        html_content += f'<h2 style="margin-top: 40px;">Key Indicator Trends ({start_year}-{final_year})</h2>'
        plot_path = "key_indicators_plot.png" # Relative path for HTML
        if os.path.exists(os.path.join(self.output_dir, plot_path)):
            html_content += f'<img src="{plot_path}" alt="Key Indicator Trends Plot">\n' 
        else:
             html_content += f'<p>(Plot image not found: {plot_path})</p>'

        # --- Footer --- 
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html_content += f"""
            <div class="footer">
                Report generated on: {timestamp}
            </div>
            </div> <!-- Close container -->
            </body>
            </html>
        """

        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Enhanced HTML report saved to {report_filename}")
        except IOError as e:
            print(f"Error writing HTML report: {e}")

# --- Main Simulation Environment ---
class BangladeshUrbanDevelopmentSimulation:
    """Main simulation environment integrating all component models."""
    def __init__(self, config):
        self.initial_config = config # Keep initial state for comparison
        print("Initializing Simulation Components...")
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
        print("\nBangladeshUrbanDevelopmentSimulation Initialized" + "\n" + "="*40)

    def run_simulation(self, analysis_engine, years=10, scenarios=None):
        """Execute simulation for the specified number of years, recording state annually."""
        print(f"Starting Simulation Run: {years} years (2025-{2025 + years -1})")
        if scenarios:
            print(f"Applying Scenarios: {scenarios}") # Placeholder

        start_year = 2025
        end_year = start_year + years

        # Record initial state (optional, useful for comparison)
        # analysis_engine.record_state(start_year - 1) # Or record after year 2025 runs

        for year in range(start_year, end_year):
            print(f"\n--- Simulating Year {year} ---")

            # Get states needed for dependencies (using getter methods)
            population_data = self.urban_growth.get_population()
            land_use_data = self.urban_growth.get_land_use()
            infrastructure_state = self.urban_infrastructure.get_infrastructure_state()
            transport_state = self.urban_transport.get_transport_state()
            economy_state = self.urban_economy.get_economy_state()
            governance_state = self.urban_governance.get_governance_state()
            environment_state = self.urban_environment.get_environment_state()
            social_state = self.urban_social.get_social_state()
            housing_state = { # Combine housing metrics for easier access
                'housing_stock': self.urban_housing.get_housing_stock(),
                'prices': self.urban_housing.get_prices(),
                'rents': self.urban_housing.get_rents(),
                'affordability': self.urban_housing.get_affordability()
            }
            service_state = self.urban_service.get_service_state()
            smart_city_state = self.smart_city.get_smart_city_state()
            # resilience_state = self.urban_resilience.get_resilience_state()

            # Run simulation steps for each component model, passing dependencies
            self.urban_growth.simulate_step(year)
            self.urban_housing.simulate_step(year, population_data, economy_state)
            self.urban_infrastructure.simulate_step(year, population_data, governance_state)
            self.urban_transport.simulate_step(year, population_data, infrastructure_state, land_use_data)
            self.urban_economy.simulate_step(year, population_data, infrastructure_state)
            self.urban_governance.simulate_step(year, infrastructure_state, social_state)
            self.urban_environment.simulate_step(year, population_data, transport_state, land_use_data, infrastructure_state)
            self.urban_social.simulate_step(year, population_data, economy_state, governance_state, service_state)
            self.urban_rural_linkage.simulate_step(year, economy_state, transport_state, housing_state)
            self.urban_service.simulate_step(year, population_data, governance_state)
            self.smart_city.simulate_step(year, infrastructure_state, social_state)
            self.urban_resilience.simulate_step(year, governance_state, environment_state)

            self.current_year = year
            # Record state at the end of each year
            analysis_engine.record_state(year)

        print("\n" + "="*40 + "\nSimulation Run Complete.")

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Initialize Data Handler
    data_handler = UrbanDataHandler()
    config = data_handler.get_config()

    # 2. Initialize Main Simulation Environment
    simulation = BangladeshUrbanDevelopmentSimulation(config)

    # 3. Initialize Analysis Engine
    analysis_engine = UrbanAnalysisEngine(simulation)

    # 4. Run the Simulation (pass analysis_engine to record state)
    num_years = 10
    simulation.run_simulation(analysis_engine, years=num_years)

    # 5. Analyze and Report Results
    # analysis_engine.generate_urban_performance_metrics(simulation.current_year) # Can enhance this method
    # analysis_engine.analyze_urbanization_dynamics() # Can enhance this method

    analysis_engine.generate_plots()
    analysis_engine.generate_html_report()

    print("\n--- Final State Example (from main script) ---")
    final_year = simulation.current_year
    print(f"Final Year: {final_year}")
    print("Final Dhaka Population:", simulation.urban_growth.population.get('Dhaka'))
    print("Final Dhaka AQI:", simulation.urban_environment.aqi.get('Dhaka'))
    print("Final Dhaka Affordability Ratio:", simulation.urban_housing.affordability.get('Dhaka')) 
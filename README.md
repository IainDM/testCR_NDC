# Costa Rica NDC Energy System Analysis

Replication of key figures from Costa Rica's **Updated Nationally Determined Contribution (NDC 2020)** and **National Decarbonization Plan 2018-2050**.

## Key NDC Figures Replicated

### Emissions Targets
| Indicator | Value | Source |
|---|---|---|
| **2030 net emissions ceiling** | **9.11 MtCO₂e** (incl. LULUCF) | Updated NDC 2020 |
| 2021-2030 cumulative budget | 106.53 MtCO₂e | Updated NDC 2020 |
| 2030 reduction vs 2015 (excl. LULUCF) | 10-14% | Updated NDC 2020 |
| **2050 net zero** | 0 MtCO₂e (5.5 gross - 5.5 LULUCF sink) | National Decarbonization Plan |

### Energy & Electricity
| Indicator | Value | Source |
|---|---|---|
| Renewable electricity share (2022) | 99.0% | ICE/CENCE |
| Renewable electricity share (2023) | 94.9% (drought) | ICE/CENCE |
| **2030 target** | **100% renewable electricity** | NDC/VII National Energy Plan |
| Total generation (2022) | ~12,525 GWh | ICE/CENCE |
| Installed capacity (2022) | 3,518 MW (89% renewable) | IRENA/ICE |
| PEG 2040 target | 5,637 MW (100% renewable) | ICE PEG 2022-2040 |
| Oil share of TPES (2018) | 53% | IEA |
| No coal or natural gas in TPES | — | IEA |

### Transport Decarbonization
| Target | Year | Source |
|---|---|---|
| 8% EV light vehicle fleet | 2030 | Updated NDC 2020 |
| 30% EV light fleet | 2035 | National Decarbonization Plan |
| 70% EV bus fleet | 2035 | National Decarbonization Plan |
| 95% zero-emission vehicles | 2050 | National Decarbonization Plan |
| Black carbon -20% vs 2018 | 2030 | Updated NDC 2020 |

### Sector Emissions (2021, excl. LULUCF)
| Sector | MtCO₂e | Share |
|---|---|---|
| Energy (total) | 7.66 | 50.9% |
| — Transport | 5.84 | 38.8% |
| — Manufacturing & Construction | 1.24 | 8.2% |
| — Buildings | 0.42 | 2.8% |
| Agriculture | 3.74 | 24.8% |
| Waste | 2.18 | 14.5% |
| IPPU | 1.47 | 9.8% |
| **Total (excl. LULUCF)** | **15.05** | **100%** |
| LULUCF (net sink) | -3.0 | — |

## Generated Figures

| # | Figure | Description |
|---|---|---|
| 01 | `ghg_emissions_by_sector.png` | Stacked area chart of GHG emissions by sector (2005-2021) |
| 02 | `ghg_sector_pie_2021.png` | Sector breakdown pie charts (overall + energy sub-sectors) |
| 03 | `electricity_generation_mix.png` | Stacked bar chart with renewable share trend (2015-2023) |
| 04 | `electricity_pie_2022_2023.png` | Side-by-side generation mix: 2022 (normal) vs 2023 (drought) |
| 05 | `tpes_breakdown.png` | Total Primary Energy Supply showing oil dominance paradox |
| 06 | `ndc_emissions_pathway.png` | Historical→NDC→Net Zero emissions trajectory |
| 07 | `transport_decarbonization.png` | Transport emissions, EV targets, black carbon reduction |
| 08 | `installed_capacity.png` | Current capacity and PEG 2022-2040 expansion plan |
| 09 | `ndc_summary_dashboard.png` | Dashboard of all key NDC targets and indicators |
| 10 | `agriculture_waste.png` | Methane sources and non-energy sector reduction targets |

## Data Sources

- **Costa Rica Updated NDC (December 2020)** — UNFCCC NDC Registry
- **National Decarbonization Plan 2018-2050** — Government of Costa Rica / MINAE
- **2nd Biennial Update Report (BUR2, 2019)** — UNFCCC
- **Climate Action Tracker** — [climateactiontracker.org/countries/costa-rica](https://climateactiontracker.org/countries/costa-rica/)
- **IRENA Renewable Energy Statistics** — [irena.org](https://www.irena.org/)
- **ICE/CENCE** — Costa Rican Electricity Institute operational data
- **Climate Watch / WRI** — [climatewatchdata.org](https://www.climatewatchdata.org/)
- **IEA** — [iea.org/countries/costa-rica](https://www.iea.org/countries/costa-rica)
- **Our World in Data** — [ourworldindata.org/energy/country/costa-rica](https://ourworldindata.org/energy/country/costa-rica)

## How to Run

```bash
pip install -r requirements.txt
python costa_rica_ndc_energy_analysis.py
```

Figures are saved to `figures/`. Data files are in `data/`.

## Project Structure

```
testCR_NDC/
├── costa_rica_ndc_energy_analysis.py   # Main analysis script
├── requirements.txt                     # Python dependencies
├── README.md                           # This file
├── data/                               # Source data (CSV)
│   ├── ghg_emissions_by_sector.csv
│   ├── electricity_generation_GWh.csv
│   ├── installed_capacity_MW.csv
│   ├── ndc_targets.csv
│   └── tpes_PJ.csv
└── figures/                            # Generated visualizations
    ├── 01_ghg_emissions_by_sector.png
    ├── 02_ghg_sector_pie_2021.png
    ├── 03_electricity_generation_mix.png
    ├── 04_electricity_pie_2022_2023.png
    ├── 05_tpes_breakdown.png
    ├── 06_ndc_emissions_pathway.png
    ├── 07_transport_decarbonization.png
    ├── 08_installed_capacity.png
    ├── 09_ndc_summary_dashboard.png
    └── 10_agriculture_waste.png
```

## Notes on Data Quality

- GHG emissions figures for 2021 are from Climate Watch/WRI and align with the national GHG inventory submitted to the UNFCCC.
- The 2015 reference year data comes from the 2nd Biennial Update Report.
- Electricity generation figures are estimates based on reported percentage shares and total generation from ICE/CENCE and IRENA.
- TPES data is estimated from IEA and Our World in Data, as granular official figures require subscription access.
- The NDC does not provide a sector-by-sector breakdown of the 9.11 MtCO₂e 2030 target; projections are based on the National Decarbonization Plan trajectory.

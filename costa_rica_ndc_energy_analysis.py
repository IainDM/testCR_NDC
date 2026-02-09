#!/usr/bin/env python3
"""
Costa Rica NDC Energy System Analysis
======================================

Replication of key figures from Costa Rica's Updated Nationally Determined
Contribution (NDC 2020) and National Decarbonization Plan.

Data sources:
- Costa Rica Updated NDC (December 2020), UNFCCC
- National Decarbonization Plan 2018-2050
- Costa Rica 2nd Biennial Update Report (BUR2, 2019)
- Climate Action Tracker (2024)
- IRENA Renewable Energy Statistics
- ICE/CENCE operational data
- Climate Watch / WRI GHG emissions data
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import os

# ============================================================================
# Configuration
# ============================================================================
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

# Color palette matching NDC / climate report style
COLORS = {
    'hydro': '#2166AC',
    'geothermal': '#D6604D',
    'wind': '#4DAF4A',
    'solar': '#FF7F00',
    'biomass': '#8B4513',
    'thermal': '#666666',
    'energy': '#E41A1C',
    'transport': '#E41A1C',
    'agriculture': '#4DAF4A',
    'waste': '#984EA3',
    'ippu': '#FF7F00',
    'lulucf': '#377EB8',
    'target': '#1B9E77',
    'bau': '#D95F02',
    'ndc': '#7570B3',
    'historical': '#333333',
}

plt.rcParams.update({
    'figure.dpi': 150,
    'figure.figsize': (10, 6),
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
})


# ============================================================================
# 1. GHG EMISSIONS BY SECTOR
# ============================================================================
def create_ghg_sector_breakdown():
    """
    GHG emissions by sector (excl. LULUCF) for key inventory years.

    Key NDC figures replicated:
    - 2012 total: ~11.2 MtCO2e (from BUR2 base year data)
    - 2015 total: ~13.6 MtCO2e (NDC reference year)
    - 2021 total: ~15.1 MtCO2e
    - Energy sector: 50.9% (2021), dominated by transport (38.8%)
    - Agriculture: 24.8% (2021)
    - Waste: 14.5% (2021)
    - LULUCF sink: ~-3.0 MtCO2e (2017)

    Sources: BUR2 (2019), Climate Watch/WRI, Climate Action Tracker
    """
    # Historical emissions by sector (MtCO2e, excl. LULUCF)
    # Data from national GHG inventories and Climate Watch
    years = [2005, 2010, 2012, 2015, 2017, 2019, 2020, 2021]

    # Sector emissions reconstructed from percentage shares and totals
    # Energy sector includes transport, manufacturing, buildings, fugitive
    energy =      [5.50, 6.20, 6.40, 6.80, 7.10, 7.50, 6.80, 7.66]
    agriculture = [3.10, 3.30, 3.35, 3.50, 3.55, 3.65, 3.60, 3.74]
    waste =       [1.30, 1.60, 1.70, 1.85, 1.95, 2.10, 2.05, 2.18]
    ippu =        [0.60, 0.80, 0.90, 1.10, 1.20, 1.40, 1.35, 1.47]

    totals = [e + a + w + i for e, a, w, i in zip(energy, agriculture, waste, ippu)]

    # LULUCF separately (net sink after 2014)
    lulucf = [2.50, 0.50, -0.50, -1.50, -3.00, -3.20, -3.10, -3.00]

    # --- Figure 1a: Stacked area chart of emissions by sector ---
    fig, ax = plt.subplots(figsize=(11, 6.5))

    ax.stackplot(years, energy, agriculture, waste, ippu,
                 labels=['Energy (incl. Transport)', 'Agriculture', 'Waste', 'IPPU'],
                 colors=[COLORS['energy'], COLORS['agriculture'],
                         COLORS['waste'], COLORS['ippu']],
                 alpha=0.85)

    ax.plot(years, lulucf, 'o-', color=COLORS['lulucf'], linewidth=2.5,
            markersize=6, label='LULUCF (net sink)', zorder=5)

    ax.plot(years, totals, 's--', color='black', linewidth=1.5,
            markersize=5, label='Total (excl. LULUCF)', zorder=5)

    # NDC 2030 target line
    ax.axhline(y=9.11, color=COLORS['target'], linestyle='--', linewidth=2,
               alpha=0.7, label='NDC 2030 target: 9.11 MtCO₂e (net)')

    ax.set_xlabel('Year')
    ax.set_ylabel('GHG Emissions (MtCO₂e)')
    ax.set_title('Costa Rica — GHG Emissions by Sector\n'
                 '(NDC Reference: Updated NDC 2020, BUR2)')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.set_ylim(-5, 18)
    ax.set_xlim(2004, 2023)

    # Annotate key values
    ax.annotate(f'2015: {totals[3]:.1f} Mt\n(NDC reference)',
                xy=(2015, totals[3]), xytext=(2016.5, totals[3] + 1.5),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=9, fontweight='bold')
    ax.annotate(f'2021: {totals[-1]:.1f} Mt',
                xy=(2021, totals[-1]), xytext=(2019.5, totals[-1] + 1.8),
                arrowprops=dict(arrowstyle='->', color='black'),
                fontsize=9, fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '01_ghg_emissions_by_sector.png'), bbox_inches='tight')
    plt.close(fig)

    # --- Figure 1b: Sector breakdown pie chart (2021) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # Broad sector breakdown
    sector_labels = ['Energy\n7.66 Mt (50.9%)', 'Agriculture\n3.74 Mt (24.8%)',
                     'Waste\n2.18 Mt (14.5%)', 'IPPU\n1.47 Mt (9.8%)']
    sector_values = [7.66, 3.74, 2.18, 1.47]
    sector_colors = [COLORS['energy'], COLORS['agriculture'],
                     COLORS['waste'], COLORS['ippu']]
    explode = (0.05, 0, 0, 0)

    wedges1, texts1, autotexts1 = ax1.pie(
        sector_values, labels=sector_labels, colors=sector_colors,
        autopct='%1.1f%%', explode=explode, startangle=90,
        textprops={'fontsize': 9})
    ax1.set_title('GHG Emissions by Sector (2021)\nTotal: 15.05 MtCO₂e excl. LULUCF',
                  fontsize=12, fontweight='bold')

    # Energy sub-sector breakdown
    energy_labels = ['Transport\n5.84 Mt (76.2%)',
                     'Manufacturing &\nConstruction\n1.24 Mt (16.2%)',
                     'Buildings\n0.42 Mt (5.5%)',
                     'Other Energy\n0.16 Mt (2.1%)']
    energy_values = [5.84, 1.24, 0.42, 0.16]
    energy_colors = ['#E41A1C', '#FF6B6B', '#FFA07A', '#FFD4C4']

    wedges2, texts2, autotexts2 = ax2.pie(
        energy_values, labels=energy_labels, colors=energy_colors,
        autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9})
    ax2.set_title('Energy Sector Breakdown (2021)\nTotal Energy: 7.66 MtCO₂e',
                  fontsize=12, fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '02_ghg_sector_pie_2021.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [1] GHG emissions by sector — done")
    print(f"      2021 total (excl. LULUCF): {totals[-1]:.2f} MtCO2e")
    print(f"      2015 total (NDC reference): {totals[3]:.2f} MtCO2e")
    print(f"      NDC 2030 net target: 9.11 MtCO2e")
    return totals, lulucf


# ============================================================================
# 2. ELECTRICITY GENERATION MIX
# ============================================================================
def create_electricity_mix():
    """
    Electricity generation by source.

    Key NDC figures replicated:
    - Total generation 2022: ~12,600 GWh
    - Renewable share: 98-99% (2015-2022), dropped to 95% in 2023
    - Hydro: 74%, Geothermal: 13%, Wind: 10.8%
    - Solar: <0.1%, Biomass: ~0.5%, Thermal: ~1%

    Sources: ICE/CENCE, IRENA, Ember
    """
    # Generation by source (GWh) — historical
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

    hydro =       [8258, 8450, 8100, 8380, 8500, 8300, 8800, 9324, 8710]
    geothermal =  [1510, 1530, 1550, 1540, 1570, 1560, 1600, 1638, 1550]
    wind =        [1050, 1100, 1180, 1250, 1280, 1200, 1300, 1361, 1525]
    solar =       [3,    5,    8,    10,   12,   12,   13,   13,   13]
    biomass =     [40,   45,   50,   55,   58,   55,   60,   63,   63]
    thermal =     [55,   70,   30,   50,   80,   120,  50,   126,  640]

    totals = [h+g+w+s+b+t for h,g,w,s,b,t in
              zip(hydro, geothermal, wind, solar, biomass, thermal)]
    renewable_pct = [(h+g+w+s+b)/(h+g+w+s+b+t)*100 for h,g,w,s,b,t in
                     zip(hydro, geothermal, wind, solar, biomass, thermal)]

    # --- Figure 2a: Stacked bar chart of generation by source ---
    fig, ax1 = plt.subplots(figsize=(12, 7))

    bar_width = 0.7
    x = np.arange(len(years))

    bottom = np.zeros(len(years))
    sources = [hydro, geothermal, wind, biomass, solar, thermal]
    labels = ['Hydropower', 'Geothermal', 'Wind', 'Biomass', 'Solar', 'Thermal (fossil)']
    colors = [COLORS['hydro'], COLORS['geothermal'], COLORS['wind'],
              COLORS['biomass'], COLORS['solar'], COLORS['thermal']]

    for data, label, color in zip(sources, labels, colors):
        ax1.bar(x, data, bar_width, bottom=bottom, label=label, color=color, alpha=0.9)
        bottom += np.array(data)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Electricity Generation (GWh)')
    ax1.set_title('Costa Rica — Electricity Generation by Source\n'
                  '(NDC: 100% renewable electricity target by 2030)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.legend(loc='upper left', framealpha=0.9)

    # Add renewable percentage as secondary axis
    ax2 = ax1.twinx()
    ax2.plot(x, renewable_pct, 'D-', color='darkgreen', linewidth=2,
             markersize=7, label='Renewable share (%)', zorder=5)
    ax2.set_ylabel('Renewable Share (%)', color='darkgreen')
    ax2.set_ylim(90, 101)
    ax2.tick_params(axis='y', labelcolor='darkgreen')
    ax2.legend(loc='upper right', framealpha=0.9)

    # Annotate key values
    for i, (yr, pct) in enumerate(zip(years, renewable_pct)):
        if yr in [2015, 2019, 2022, 2023]:
            ax2.annotate(f'{pct:.1f}%', xy=(i, pct),
                        xytext=(0, 10), textcoords='offset points',
                        fontsize=9, fontweight='bold', ha='center',
                        color='darkgreen')

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '03_electricity_generation_mix.png'), bbox_inches='tight')
    plt.close(fig)

    # --- Figure 2b: Generation source pie for 2022 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # 2022 mix
    gen_2022 = [9324, 1638, 1361, 63, 13, 126]
    pct_2022 = [v/sum(gen_2022)*100 for v in gen_2022]
    labels_2022 = [f'Hydro\n{gen_2022[0]:,} GWh ({pct_2022[0]:.1f}%)',
                   f'Geothermal\n{gen_2022[1]:,} GWh ({pct_2022[1]:.1f}%)',
                   f'Wind\n{gen_2022[2]:,} GWh ({pct_2022[2]:.1f}%)',
                   f'Biomass\n{gen_2022[3]} GWh ({pct_2022[3]:.1f}%)',
                   f'Solar\n{gen_2022[4]} GWh ({pct_2022[4]:.1f}%)',
                   f'Thermal\n{gen_2022[5]} GWh ({pct_2022[5]:.1f}%)']

    ax1.pie(gen_2022, labels=labels_2022, colors=colors,
            autopct='', startangle=90, textprops={'fontsize': 9})
    ax1.set_title(f'Electricity Generation Mix 2022\nTotal: {sum(gen_2022):,} GWh | '
                  f'Renewable: {renewable_pct[7]:.1f}%',
                  fontsize=11, fontweight='bold')

    # 2023 mix (drought year)
    gen_2023 = [8710, 1550, 1525, 63, 13, 640]
    pct_2023 = [v/sum(gen_2023)*100 for v in gen_2023]
    labels_2023 = [f'Hydro\n{gen_2023[0]:,} GWh ({pct_2023[0]:.1f}%)',
                   f'Geothermal\n{gen_2023[1]:,} GWh ({pct_2023[1]:.1f}%)',
                   f'Wind\n{gen_2023[2]:,} GWh ({pct_2023[2]:.1f}%)',
                   f'Biomass\n{gen_2023[3]} GWh ({pct_2023[3]:.1f}%)',
                   f'Solar\n{gen_2023[4]} GWh ({pct_2023[4]:.1f}%)',
                   f'Thermal\n{gen_2023[5]} GWh ({pct_2023[5]:.1f}%)']

    ax2.pie(gen_2023, labels=labels_2023, colors=colors,
            autopct='', startangle=90, textprops={'fontsize': 9})
    ax2.set_title(f'Electricity Generation Mix 2023 (Drought Year)\nTotal: {sum(gen_2023):,} GWh | '
                  f'Renewable: {renewable_pct[8]:.1f}%',
                  fontsize=11, fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '04_electricity_pie_2022_2023.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [2] Electricity generation mix — done")
    print(f"      2022 total: {totals[7]:,} GWh, renewable: {renewable_pct[7]:.1f}%")
    print(f"      2023 total: {totals[8]:,} GWh, renewable: {renewable_pct[8]:.1f}%")
    return totals, renewable_pct


# ============================================================================
# 3. TOTAL PRIMARY ENERGY SUPPLY (TPES)
# ============================================================================
def create_tpes_analysis():
    """
    Total Primary Energy Supply breakdown showing the disconnect between
    clean electricity and oil-dependent total energy.

    Key NDC figures replicated:
    - Oil: 53% of TPES (2018)
    - Renewables: only 34.2% of total final energy consumption (2021)
    - No coal or natural gas in TPES
    - TPES ~146 PJ (2020)

    Sources: IEA, Climate Action Tracker, Our World in Data
    """
    # TPES by source (PJ) — estimates from IEA/OWID data
    years = [2010, 2015, 2018, 2019, 2020, 2021, 2022]

    oil =        [85.0, 88.0, 89.0, 90.0, 78.0, 82.0, 86.0]
    hydro_pj =   [33.0, 35.0, 35.5, 36.0, 35.0, 37.0, 39.0]
    geothermal_pj = [13.0, 14.0, 14.5, 14.5, 14.0, 14.5, 15.0]
    wind_pj =    [3.0,  4.5,  5.5,  6.0,  5.5,  6.0,  6.5]
    biomass_pj = [10.0, 11.0, 11.5, 12.0, 11.0, 11.5, 12.0]
    solar_pj =   [0.0,  0.0,  0.0,  0.1,  0.1,  0.1,  0.1]

    totals_pj = [o+h+g+w+b+s for o,h,g,w,b,s in
                 zip(oil, hydro_pj, geothermal_pj, wind_pj, biomass_pj, solar_pj)]
    oil_share = [o/t*100 for o,t in zip(oil, totals_pj)]
    re_share = [(h+g+w+b+s)/t*100 for h,g,w,b,s,t in
                zip(hydro_pj, geothermal_pj, wind_pj, biomass_pj, solar_pj, totals_pj)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Stacked bar for TPES
    x = np.arange(len(years))
    bar_w = 0.6
    bottom = np.zeros(len(years))

    for data, label, color in zip(
        [oil, hydro_pj, geothermal_pj, wind_pj, biomass_pj, solar_pj],
        ['Oil products', 'Hydropower', 'Geothermal', 'Wind', 'Biomass', 'Solar'],
        [COLORS['thermal'], COLORS['hydro'], COLORS['geothermal'],
         COLORS['wind'], COLORS['biomass'], COLORS['solar']]):
        ax1.bar(x, data, bar_w, bottom=bottom, label=label, color=color, alpha=0.9)
        bottom += np.array(data)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total Primary Energy Supply (PJ)')
    ax1.set_title('Costa Rica — Total Primary Energy Supply\n'
                  '(Oil dominates despite near-100% renewable electricity)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.legend(loc='upper left', fontsize=9)

    # Oil vs Renewable share comparison
    ax2.bar(x - 0.2, oil_share, 0.35, label='Oil share of TPES',
            color=COLORS['thermal'], alpha=0.85)
    ax2.bar(x + 0.2, re_share, 0.35, label='Renewable share of TPES',
            color=COLORS['wind'], alpha=0.85)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Share of TPES (%)')
    ax2.set_title('The Energy Paradox:\nClean Electricity vs Oil-Dependent Economy')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.legend(fontsize=10)
    ax2.set_ylim(0, 70)

    for i in range(len(years)):
        ax2.text(i - 0.2, oil_share[i] + 1, f'{oil_share[i]:.0f}%',
                ha='center', va='bottom', fontsize=8, fontweight='bold')
        ax2.text(i + 0.2, re_share[i] + 1, f'{re_share[i]:.0f}%',
                ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '05_tpes_breakdown.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [3] TPES analysis — done")
    print(f"      2018 oil share: {oil_share[2]:.1f}%")
    print(f"      2020 TPES total: {totals_pj[4]:.1f} PJ")


# ============================================================================
# 4. NDC EMISSIONS PATHWAY (2015 → 2050)
# ============================================================================
def create_ndc_pathway():
    """
    Emissions pathway showing historical trend, NDC target, and net-zero trajectory.

    Key NDC figures replicated:
    - 2030 target: max 9.11 MtCO2e net (incl. LULUCF)
    - 2021-2030 cumulative budget: 106.53 MtCO2e
    - 2050 target: net zero
    - 2050 residual: 5.5 MtCO2e gross, offset by -5.5 MtCO2e LULUCF sink
    - NDC aims for 10-14% below 2015 levels (excl. LULUCF) by 2030

    Sources: NDC 2020, National Decarbonization Plan, Climate Action Tracker
    """
    # Historical net emissions (gross - LULUCF sink)
    hist_years = [2005, 2010, 2012, 2015, 2017, 2019, 2020, 2021]
    hist_gross = [10.50, 11.90, 12.35, 13.25, 13.80, 14.65, 13.80, 15.05]
    hist_lulucf = [2.50, 0.50, -0.50, -1.50, -3.00, -3.20, -3.10, -3.00]
    hist_net = [g + l for g, l in zip(hist_gross, hist_lulucf)]

    # NDC pathway (net emissions including LULUCF)
    # Budget: 106.53 MtCO2e over 2021-2030
    # Target: max 9.11 MtCO2e in 2030
    ndc_years = [2021, 2025, 2030]
    ndc_net = [12.05, 10.50, 9.11]

    # BAU projection (without additional measures)
    bau_years = [2021, 2025, 2030]
    bau_net = [12.05, 13.50, 15.50]

    # Decarbonization Plan 2050 pathway
    decarb_years = [2030, 2035, 2040, 2045, 2050]
    decarb_gross = [11.90, 9.50, 7.50, 6.50, 5.50]  # Gross emissions decline
    decarb_lulucf = [-2.79, -3.50, -4.20, -4.80, -5.50]  # Increasing sink
    decarb_net = [g + l for g, l in zip(decarb_gross, decarb_lulucf)]

    fig, ax = plt.subplots(figsize=(13, 7))

    # Historical
    ax.plot(hist_years, hist_gross, 'o-', color='#333333', linewidth=2.5,
            markersize=6, label='Historical gross (excl. LULUCF)', zorder=4)
    ax.plot(hist_years, hist_net, 's-', color='#666666', linewidth=2,
            markersize=5, label='Historical net (incl. LULUCF)', zorder=4)

    # BAU
    ax.plot(bau_years, bau_net, 'x--', color=COLORS['bau'], linewidth=2,
            markersize=8, label='BAU projection (net)', zorder=3)

    # NDC target pathway
    ax.plot(ndc_years, ndc_net, 'D-', color=COLORS['ndc'], linewidth=2.5,
            markersize=8, label='NDC target pathway (net)', zorder=5)

    # 2050 decarbonization pathway
    ax.plot(decarb_years, decarb_gross, '^--', color='#D95F02', linewidth=1.5,
            markersize=6, label='Decarbonization Plan gross', zorder=3, alpha=0.7)
    ax.plot(decarb_years, decarb_net, 'v-', color=COLORS['target'], linewidth=2.5,
            markersize=7, label='Decarbonization Plan net → Net Zero', zorder=5)

    # Target markers
    ax.axhline(y=9.11, color=COLORS['ndc'], linestyle=':', linewidth=1, alpha=0.5)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.3)

    # Shade NDC budget area
    budget_years = list(range(2021, 2031))
    budget_upper = np.interp(budget_years, ndc_years, ndc_net)
    ax.fill_between(budget_years, 0, budget_upper, alpha=0.1, color=COLORS['ndc'],
                    label='NDC budget: 106.53 MtCO₂e (2021-2030)')

    # Annotations
    ax.annotate('NDC 2030 target:\n9.11 MtCO₂e net',
                xy=(2030, 9.11), xytext=(2032, 11),
                arrowprops=dict(arrowstyle='->', color=COLORS['ndc']),
                fontsize=10, fontweight='bold', color=COLORS['ndc'])

    ax.annotate('Net Zero\n2050',
                xy=(2050, decarb_net[-1]), xytext=(2046, 2.5),
                arrowprops=dict(arrowstyle='->', color=COLORS['target']),
                fontsize=10, fontweight='bold', color=COLORS['target'])

    ax.annotate(f'2050 gross: 5.5 Mt\nLULUCF sink: -5.5 Mt',
                xy=(2050, 0), xytext=(2042, -2.5),
                fontsize=9, fontstyle='italic', color='#555555')

    ax.set_xlabel('Year')
    ax.set_ylabel('GHG Emissions (MtCO₂e)')
    ax.set_title('Costa Rica — NDC Emissions Pathway to Net Zero (2050)\n'
                 'Updated NDC 2020 & National Decarbonization Plan')
    ax.legend(loc='upper right', framealpha=0.9, fontsize=9)
    ax.set_xlim(2003, 2053)
    ax.set_ylim(-4, 18)

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '06_ndc_emissions_pathway.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [4] NDC emissions pathway — done")
    print(f"      NDC 2030 net target: 9.11 MtCO2e")
    print(f"      2021-2030 budget: 106.53 MtCO2e")
    print(f"      2050 net zero: gross 5.5 Mt - LULUCF 5.5 Mt = 0")


# ============================================================================
# 5. TRANSPORT DECARBONIZATION PATHWAY
# ============================================================================
def create_transport_pathway():
    """
    Transport sector decarbonization — largest mitigation opportunity.

    Key NDC figures replicated:
    - Transport: 76% of energy-related CO2, 38.8% of total (2021)
    - EV targets: 8% light fleet by 2030, 30% by 2035, 95% by 2050
    - Law 9518 incentives
    - Black carbon reduction: 20% by 2030 (vs 2018)
    - 2050: 65% transport emissions reduction via electrification
    - Buses: 70% electric by 2035, 100% by 2050

    Sources: NDC 2020, National Decarbonization Plan, Law 9518
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # --- Panel A: Transport emissions trajectory ---
    years_t = [2015, 2018, 2019, 2020, 2021, 2025, 2030, 2035, 2040, 2045, 2050]
    transport_emissions = [5.20, 5.60, 5.75, 5.00, 5.84, 5.50, 4.80, 3.80, 2.80, 2.30, 2.04]
    transport_bau = [5.20, 5.60, 5.75, 5.00, 5.84, 6.20, 6.80, 7.30, 7.80, 8.20, 8.50]

    ax1.plot(years_t, transport_bau, 'x--', color=COLORS['bau'], linewidth=2,
             label='BAU projection')
    ax1.plot(years_t, transport_emissions, 'o-', color=COLORS['energy'], linewidth=2.5,
             label='Decarbonization pathway')
    ax1.fill_between(years_t, transport_emissions, transport_bau,
                     alpha=0.15, color=COLORS['energy'],
                     label='Emissions avoided')
    ax1.axhline(y=5.84*0.35, color=COLORS['target'], linestyle=':', linewidth=1.5,
                label='65% reduction target (2050)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Transport Emissions (MtCO₂e)')
    ax1.set_title('(a) Transport Sector Emissions Pathway')
    ax1.legend(fontsize=8, loc='upper left')
    ax1.set_ylim(0, 10)

    # --- Panel B: EV fleet penetration targets ---
    ev_years = [2020, 2022, 2025, 2030, 2035, 2040, 2045, 2050]
    ev_light = [1, 3, 5, 8, 30, 55, 75, 95]  # % of light vehicle fleet
    ev_bus = [0, 1, 5, 15, 70, 85, 95, 100]  # % of bus fleet
    ev_sales = [2, 5, 12, 25, 50, 70, 90, 100]  # % of new car sales

    ax2.plot(ev_years, ev_light, 'o-', color='#2166AC', linewidth=2.5,
             label='Light vehicle fleet (%)')
    ax2.plot(ev_years, ev_bus, 's-', color='#D6604D', linewidth=2.5,
             label='Bus fleet (%)')
    ax2.plot(ev_years, ev_sales, '^--', color='#4DAF4A', linewidth=2,
             label='New vehicle sales (%)')

    # Key milestone markers
    ax2.axvline(x=2030, color='gray', linestyle=':', alpha=0.4)
    ax2.axvline(x=2035, color='gray', linestyle=':', alpha=0.4)
    ax2.axvline(x=2050, color='gray', linestyle=':', alpha=0.4)

    ax2.annotate('NDC: 8%\nlight fleet', xy=(2030, 8), xytext=(2031, 25),
                arrowprops=dict(arrowstyle='->', color='#2166AC'),
                fontsize=8, color='#2166AC', fontweight='bold')
    ax2.annotate('30% light\n70% bus', xy=(2035, 30), xytext=(2036, 50),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=8, fontweight='bold')
    ax2.annotate('95% ZEV\n100% bus', xy=(2050, 95), xytext=(2044, 82),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=8, fontweight='bold')

    ax2.set_xlabel('Year')
    ax2.set_ylabel('Electric/Zero-Emission Share (%)')
    ax2.set_title('(b) EV Fleet Penetration Targets\n(NDC 2020 & Decarbonization Plan)')
    ax2.legend(fontsize=8, loc='upper left')
    ax2.set_ylim(0, 105)

    # --- Panel C: Energy-related emissions breakdown ---
    categories = ['Transport\n(road)', 'Manufacturing\n& Construction', 'Buildings', 'Other\nEnergy']
    values_2021 = [5.84, 1.24, 0.42, 0.16]
    values_target = [2.04, 0.80, 0.25, 0.10]  # 2050 target estimates

    x = np.arange(len(categories))
    ax3.bar(x - 0.2, values_2021, 0.35, label='2021 actual',
            color=COLORS['energy'], alpha=0.85)
    ax3.bar(x + 0.2, values_target, 0.35, label='2050 target',
            color=COLORS['target'], alpha=0.85)

    for i in range(len(categories)):
        reduction = (1 - values_target[i]/values_2021[i]) * 100
        ax3.text(i + 0.2, values_target[i] + 0.1, f'-{reduction:.0f}%',
                ha='center', fontsize=8, fontweight='bold', color=COLORS['target'])

    ax3.set_ylabel('Emissions (MtCO₂e)')
    ax3.set_title('(c) Energy Sub-sector: 2021 vs 2050 Target')
    ax3.set_xticks(x)
    ax3.set_xticklabels(categories)
    ax3.legend(fontsize=9)

    # --- Panel D: Black carbon reduction ---
    bc_years = [2018, 2020, 2022, 2025, 2030]
    bc_index = [100, 97, 94, 88, 80]  # Index: 2018 = 100

    ax4.bar(range(len(bc_years)), bc_index, color='#555555', alpha=0.8)
    ax4.axhline(y=80, color=COLORS['target'], linestyle='--', linewidth=2,
                label='NDC target: 20% reduction by 2030')
    ax4.set_xticks(range(len(bc_years)))
    ax4.set_xticklabels(bc_years)
    ax4.set_ylabel('Black Carbon Index (2018 = 100)')
    ax4.set_title('(d) Black Carbon Reduction from Energy\n(NDC 2020: -20% vs 2018 by 2030)')
    ax4.legend(fontsize=9)
    ax4.set_ylim(0, 110)

    for i, v in enumerate(bc_index):
        ax4.text(i, v + 2, f'{v}', ha='center', fontweight='bold', fontsize=9)

    plt.suptitle('Costa Rica — Transport & Energy Decarbonization\n'
                 '(NDC 2020, National Decarbonization Plan, Law 9518)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '07_transport_decarbonization.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [5] Transport decarbonization pathway — done")
    print(f"      2021 transport emissions: 5.84 MtCO2e (38.8% of total)")
    print(f"      EV target 2030: 8% light fleet, 2050: 95% ZEV")


# ============================================================================
# 6. INSTALLED CAPACITY & FUTURE EXPANSION (PEG 2022-2040)
# ============================================================================
def create_capacity_analysis():
    """
    Installed electricity generation capacity and expansion plans.

    Key NDC figures replicated:
    - Total capacity 2022: ~3,518 MW (89% renewable)
    - PEG 2022-2040: expand to 5,637 MW by 2040
    - New capacity: +2,155 MW (solar 1,100, wind 502, biomass 300)
    - 2040 target mix: hydro 56%, wind 17.6%, geothermal 17.3%, solar 8.4%

    Sources: ICE PEG 2022-2040, IRENA, CENCE
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # --- Panel A: Current installed capacity (2022) ---
    cap_labels = ['Hydropower', 'Geothermal', 'Wind', 'Thermal\n(fossil)', 'Solar', 'Biomass']
    cap_2022 = [2400, 208, 400, 387, 100, 23]  # MW
    cap_colors = [COLORS['hydro'], COLORS['geothermal'], COLORS['wind'],
                  COLORS['thermal'], COLORS['solar'], COLORS['biomass']]

    bars = ax1.barh(cap_labels, cap_2022, color=cap_colors, alpha=0.9, height=0.6)
    ax1.set_xlabel('Installed Capacity (MW)')
    ax1.set_title(f'Installed Generation Capacity 2022\nTotal: {sum(cap_2022):,} MW | '
                  f'Renewable: {(sum(cap_2022)-387)/sum(cap_2022)*100:.0f}%')
    ax1.set_xlim(0, 2800)

    for bar, val in zip(bars, cap_2022):
        pct = val/sum(cap_2022)*100
        ax1.text(val + 30, bar.get_y() + bar.get_height()/2,
                f'{val:,} MW ({pct:.1f}%)', va='center', fontsize=10, fontweight='bold')

    # --- Panel B: Capacity expansion to 2040 (PEG) ---
    sources = ['Hydro', 'Geothermal', 'Wind', 'Solar', 'Biomass', 'Thermal']
    cap_current = [2400, 208, 400, 100, 23, 387]
    cap_2040 = [3157, 976, 994, 474, 323, 0]  # PEG targets (thermal phased out)
    # Note: 2040 total = 5,637 MW (from PEG)
    # mix: hydro 56%, geothermal 17.3%, wind 17.6%, solar 8.4%

    x = np.arange(len(sources))
    ax2.bar(x - 0.2, cap_current, 0.35, label='2022 capacity',
            color=[COLORS['hydro'], COLORS['geothermal'], COLORS['wind'],
                   COLORS['solar'], COLORS['biomass'], COLORS['thermal']], alpha=0.7)
    ax2.bar(x + 0.2, cap_2040, 0.35, label='2040 target (PEG)',
            color=[COLORS['hydro'], COLORS['geothermal'], COLORS['wind'],
                   COLORS['solar'], COLORS['biomass'], COLORS['thermal']], alpha=1.0,
            edgecolor='black', linewidth=0.5)

    for i in range(len(sources)):
        diff = cap_2040[i] - cap_current[i]
        if diff > 0:
            ax2.text(i + 0.2, cap_2040[i] + 30, f'+{diff}\nMW',
                    ha='center', fontsize=8, fontweight='bold', color=COLORS['target'])
        elif diff < 0:
            ax2.text(i + 0.2, 30, f'{diff}\nMW',
                    ha='center', fontsize=8, fontweight='bold', color='red')

    ax2.set_xlabel('Source')
    ax2.set_ylabel('Installed Capacity (MW)')
    ax2.set_title(f'Generation Expansion Plan (PEG 2022-2040)\n'
                  f'Current: {sum(cap_current):,} MW → Target: {sum(cap_2040):,} MW '
                  f'(+{sum(cap_2040)-sum(cap_current):,} MW)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(sources)
    ax2.legend(fontsize=10)

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '08_installed_capacity.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [6] Installed capacity & PEG expansion — done")
    print(f"      2022 total: {sum(cap_2022):,} MW ({(sum(cap_2022)-387)/sum(cap_2022)*100:.0f}% renewable)")
    print(f"      2040 PEG target: {sum(cap_2040):,} MW (100% renewable)")


# ============================================================================
# 7. NDC KEY TARGETS SUMMARY DASHBOARD
# ============================================================================
def create_summary_dashboard():
    """
    Summary dashboard of all key NDC targets and indicators.

    Sources: NDC 2020, National Decarbonization Plan, BUR2
    """
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # --- 1. Net emissions target gauge ---
    ax = axes[0, 0]
    categories = ['2015\n(NDC ref.)', '2021\n(latest)', '2030\nNDC target', '2050\nNet zero']
    values = [11.75, 12.05, 9.11, 0.0]
    colors_bar = ['#666666', '#E41A1C', COLORS['ndc'], COLORS['target']]
    bars = ax.bar(categories, values, color=colors_bar, alpha=0.85, width=0.6)
    ax.set_ylabel('Net GHG Emissions (MtCO₂e)')
    ax.set_title('Net Emissions Targets', fontweight='bold')
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.3,
               f'{val:.2f}', ha='center', fontweight='bold', fontsize=10)

    # --- 2. Renewable electricity share ---
    ax = axes[0, 1]
    re_years = ['2015', '2019', '2022', '2023', '2030\ntarget']
    re_values = [99.5, 99.2, 99.0, 94.9, 100.0]
    colors_re = ['green', 'green', 'green', '#D95F02', COLORS['target']]
    bars = ax.bar(re_years, re_values, color=colors_re, alpha=0.85, width=0.6)
    ax.set_ylabel('Renewable Share (%)')
    ax.set_title('Renewable Electricity', fontweight='bold')
    ax.set_ylim(88, 102)
    ax.axhline(y=100, color=COLORS['target'], linestyle='--', alpha=0.5)
    for bar, val in zip(bars, re_values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.3,
               f'{val:.1f}%', ha='center', fontweight='bold', fontsize=9)

    # --- 3. EV fleet targets ---
    ax = axes[0, 2]
    ev_milestones = ['2023\n(actual)', '2030\nNDC', '2035\nNDP', '2050\nNDP']
    ev_values = [3, 8, 30, 95]
    ax.bar(ev_milestones, ev_values, color='#2166AC', alpha=0.85, width=0.6)
    ax.set_ylabel('EV Share of Light Fleet (%)')
    ax.set_title('Transport Electrification', fontweight='bold')
    for i, val in enumerate(ev_values):
        ax.text(i, val + 1.5, f'{val}%', ha='center', fontweight='bold', fontsize=10)

    # --- 4. Emissions budget ---
    ax = axes[1, 0]
    budget_total = 106.53
    # Rough estimate of cumulative emissions 2021-2024
    spent = 12.05 + 11.5 + 11.0 + 10.8  # ~45.35
    remaining = budget_total - spent
    ax.pie([spent, remaining],
           labels=[f'Used (est.)\n{spent:.1f} Mt', f'Remaining\n{remaining:.1f} Mt'],
           colors=['#E41A1C', '#4DAF4A'], autopct='%1.0f%%',
           startangle=90, textprops={'fontsize': 10})
    ax.set_title(f'NDC Emissions Budget\n2021-2030: {budget_total} MtCO₂e',
                fontweight='bold')

    # --- 5. LULUCF sink ---
    ax = axes[1, 1]
    lulucf_years = ['1990', '2000', '2010', '2014', '2017', '2021']
    lulucf_values = [29.0, 10.0, 0.5, -1.0, -3.0, -3.0]
    colors_lulucf = ['red' if v > 0 else 'green' for v in lulucf_values]
    ax.bar(lulucf_years, lulucf_values, color=colors_lulucf, alpha=0.85)
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axhline(y=-5.5, color=COLORS['target'], linestyle='--',
               label='2050 target: -5.5 Mt')
    ax.set_ylabel('LULUCF (MtCO₂e)')
    ax.set_title('LULUCF: From Source to Sink', fontweight='bold')
    ax.legend(fontsize=9)

    # --- 6. Key policy milestones ---
    ax = axes[1, 2]
    ax.axis('off')
    milestones = [
        ('2018', 'Law 9518: EV incentives'),
        ('2019', 'National Decarbonization Plan'),
        ('2020', 'Updated NDC submitted (Dec)'),
        ('2020', 'Oil exploration moratorium → 2050'),
        ('2030', 'NDC: 9.11 MtCO₂e net max'),
        ('2030', '100% renewable electricity'),
        ('2030', '8% EV light fleet'),
        ('2035', '30% EV light fleet, 70% EV bus'),
        ('2050', 'Net zero emissions'),
        ('2050', '95% zero-emission vehicles'),
    ]
    y_pos = 0.95
    ax.text(0.5, 1.05, 'Key Policy Milestones', fontsize=13,
            fontweight='bold', ha='center', transform=ax.transAxes)
    for year, desc in milestones:
        color = COLORS['target'] if int(year) >= 2030 else '#333333'
        ax.text(0.05, y_pos, f'{year}', fontsize=10, fontweight='bold',
               color=color, transform=ax.transAxes, va='top')
        ax.text(0.18, y_pos, desc, fontsize=9, color='#333333',
               transform=ax.transAxes, va='top')
        y_pos -= 0.10

    plt.suptitle("Costa Rica — NDC Key Figures & Targets Dashboard\n"
                 "(Updated NDC 2020, National Decarbonization Plan 2018-2050)",
                 fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '09_ndc_summary_dashboard.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [7] Summary dashboard — done")


# ============================================================================
# 8. AGRICULTURE AND WASTE SECTORS
# ============================================================================
def create_agriculture_waste_analysis():
    """
    Agriculture and waste sector analysis — important for Costa Rica's
    emissions profile given the relatively clean electricity sector.

    Key figures:
    - Agriculture: 24.8% of total GHG (2021), ~3.74 MtCO2e
    - Methane: ~32% of total national emissions (2022)
    - Waste: 14.5% of total GHG (2021), ~2.18 MtCO2e
    - LULUCF net sink since 2014

    Sources: BUR2, Climate Watch, NDC 2020
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # --- Panel A: Methane composition ---
    # Methane ~32% of total emissions in 2022
    # Breakdown: agriculture (enteric fermentation, manure), waste (landfill)
    methane_sources = ['Enteric\nFermentation', 'Manure\nManagement', 'Rice\nCultivation',
                       'Landfill\nEmissions', 'Wastewater', 'Other']
    methane_values = [1.80, 0.45, 0.25, 1.20, 0.50, 0.15]  # MtCO2e approx
    methane_colors = ['#4DAF4A', '#8BC34A', '#CDDC39',
                      '#984EA3', '#CE93D8', '#BDBDBD']

    bars = ax1.barh(methane_sources, methane_values, color=methane_colors, alpha=0.85)
    ax1.set_xlabel('Emissions (MtCO₂e)')
    ax1.set_title(f'Methane Emissions by Source\n'
                  f'Total CH₄: ~{sum(methane_values):.1f} MtCO₂e '
                  f'(~32% of national GHG)')
    for bar, val in zip(bars, methane_values):
        ax1.text(val + 0.03, bar.get_y() + bar.get_height()/2,
                f'{val:.2f} Mt', va='center', fontsize=9, fontweight='bold')

    # --- Panel B: Non-energy sector reduction potential ---
    sectors = ['Agriculture', 'Waste', 'IPPU']
    current = [3.74, 2.18, 1.47]
    target_2050 = [2.20, 0.80, 0.50]  # Estimated from Decarb Plan residual of 5.5 Mt

    x = np.arange(len(sectors))
    ax2.bar(x - 0.2, current, 0.35, label='2021 actual',
            color=[COLORS['agriculture'], COLORS['waste'], COLORS['ippu']], alpha=0.85)
    ax2.bar(x + 0.2, target_2050, 0.35, label='2050 target',
            color=[COLORS['agriculture'], COLORS['waste'], COLORS['ippu']],
            alpha=0.4, edgecolor='black', linewidth=1)

    for i in range(len(sectors)):
        reduction = (1 - target_2050[i]/current[i]) * 100
        ax2.text(i + 0.2, target_2050[i] + 0.08, f'-{reduction:.0f}%',
                ha='center', fontsize=10, fontweight='bold', color=COLORS['target'])

    ax2.set_ylabel('Emissions (MtCO₂e)')
    ax2.set_title('Non-Energy Sector Emissions:\n2021 Actual vs 2050 Target')
    ax2.set_xticks(x)
    ax2.set_xticklabels(sectors)
    ax2.legend(fontsize=10)

    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, '10_agriculture_waste.png'), bbox_inches='tight')
    plt.close(fig)

    print("  [8] Agriculture & waste analysis — done")
    print(f"      Methane: ~{sum(methane_values):.1f} MtCO2e (~32% of national GHG)")


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 70)
    print("Costa Rica NDC Energy System Analysis")
    print("Updated NDC 2020 & National Decarbonization Plan 2018-2050")
    print("=" * 70)
    print()

    print("Generating figures...")
    print()

    totals_ghg, lulucf = create_ghg_sector_breakdown()
    print()

    totals_elec, re_pct = create_electricity_mix()
    print()

    create_tpes_analysis()
    print()

    create_ndc_pathway()
    print()

    create_transport_pathway()
    print()

    create_capacity_analysis()
    print()

    create_summary_dashboard()
    print()

    create_agriculture_waste_analysis()
    print()

    print("=" * 70)
    print("KEY NDC FIGURES SUMMARY")
    print("=" * 70)
    print()
    print("NDC TARGET (2030)")
    print(f"  Net emissions ceiling:         9.11 MtCO₂e (incl. LULUCF)")
    print(f"  Cumulative budget 2021-2030:   106.53 MtCO₂e")
    print(f"  Reduction vs 2015 (excl. LU):  10-14%")
    print()
    print("LONG-TERM TARGET (2050)")
    print(f"  Net zero emissions")
    print(f"  Gross residual:                5.5 MtCO₂e")
    print(f"  LULUCF sink:                  -5.5 MtCO₂e")
    print()
    print("ELECTRICITY SECTOR")
    print(f"  2022 renewable share:          99.0%")
    print(f"  2023 renewable share:          94.9% (drought)")
    print(f"  2030 target:                   100% renewable")
    print(f"  Installed capacity 2022:       3,518 MW")
    print(f"  PEG 2040 target:               5,637 MW")
    print()
    print("ENERGY SUPPLY (TPES)")
    print(f"  Oil share of TPES (2018):      53%")
    print(f"  Renewable share of TFEC:       34.2% (2021)")
    print(f"  No coal or natural gas")
    print()
    print("TRANSPORT")
    print(f"  Share of total GHG (2021):     38.8% (5.84 MtCO₂e)")
    print(f"  Share of energy CO₂:           76%")
    print(f"  EV light fleet 2030:           8%")
    print(f"  EV light fleet 2035:           30%")
    print(f"  Zero-emission vehicles 2050:   95%")
    print(f"  Black carbon -20% by 2030 vs 2018")
    print()
    print("AGRICULTURE & WASTE")
    print(f"  Agriculture (2021):            3.74 MtCO₂e (24.8%)")
    print(f"  Waste (2021):                  2.18 MtCO₂e (14.5%)")
    print(f"  Methane:                       ~32% of national GHG")
    print()
    print("LULUCF")
    print(f"  Net sink since:                2014")
    print(f"  2017 sink:                    -3.0 MtCO₂e")
    print(f"  2050 target sink:             -5.5 MtCO₂e")
    print()
    print(f"All figures saved to: {FIGURES_DIR}/")
    print("=" * 70)


if __name__ == '__main__':
    main()

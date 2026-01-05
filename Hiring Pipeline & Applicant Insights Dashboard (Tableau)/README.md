# Dev Employment Analytics

Interactive Tableau dashboard analyzing 73,462 Stack Overflow developers (53% employment rate) with dynamic threshold filtering across experience, education, and gender-age segments.

## Features
- 73,462 developer records
- Employment rate: 53% baseline
- Parameter slider: 40-70% threshold
- Breakdowns: Experience (blue), Education (orange), Gender×Age (heatmap)

## Key Insights
- **20+ years experience**: 65% employment (strongest segment)
- **Master's education**: 58% hired vs 48% NoHigherEd
- **Man <35**: Peak 55% rate (largest group 42k devs)
- **Threshold >60%**: Filters to top 25% experienced devs
- **Portfolio value**: ETL 73k CSV → parameter analytics → executive-ready

## Files
Project.twbx
data/stackoverflow_full.csv
archive.zip

## Usage
1. Download `Project.twbx`
2. Open Tableau Desktop/Public  
3. Adjust threshold slider
4. Use Filters on Experince Levels to view the changes in data

## Tech
- Tableau Public
- 73k-row CSV dataset

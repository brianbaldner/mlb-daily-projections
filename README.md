# MLB Daily Projections

This repository generates daily MLB matchup projections and an interactive plot. Every morning at 6:00 AM PST, the data is updated and published to GitHub Pages.

## Live Demo

- **Interactive Plot:** [https://mlb.brianbaldner.com](https://mlb.brianbaldner.com)
- **CSV Data:** [https://mlb.brianbaldner.com/result.csv](https://mlb.brianbaldner.com/result.csv)

## How It Works

The projections are computed by retrieving pitch data and batter statistics from MLB StatCast using custom API requests in the Python scripts. In summary:
- **Data Collection:** The script `get_game.py` pulls batter and pitcher data for the current seasons.
- **Aggregation:** Using functions in [`analysis.py`](c:\Users\bbald\OneDrive\Desktop\gambling\analysis.py) and [`functions.py`](c:\Users\bbald\OneDrive\Desktop\gambling\functions.py), pitch metrics are grouped by pitch type.
- **Projection Calculation:** The algorithm calculates the hit and base probabilities per pitch. It multiplies these by the average number of pitches per plate appearance and scales the results to a standard 5 at-bats (5ab) to derive projected hits and bases.
- **Output:** The resulting data is written to `result.csv` and an accompanying interactive plot is generated. The plot only contains hitters with over 50 PA for that hand over the last 2 seasons. The daily GitHub Actions workflow (see [`run_daily.yaml`](c:\Users\bbald\OneDrive\Desktop\gambling\.github\workflows\run_daily.yaml)) commits and pushes these changes to update the live pages.

## Features

- **Daily Automated Updates:** A GitHub Actions workflow runs every day at 6:00 AM PST.
- **Interactive Visualization:** Explore projections with a dynamic plot hosted on GitHub Pages.
- **CSV Data Output:** Download the most recent projections as CSV.
- **Modular Python Code:** Separate functions handle data retrieval, aggregation, and projection calculations.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/mlb-daily-projections.git
   cd mlb-daily-projections
   ```

2. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Usage

- **Local Testing:** Run the main script to generate projections:
  ```bash
  python get_game.py
  ```

- **Automated Deployment:** The workflow defined in [.github/workflows/run_daily.yaml](c:\Users\bbald\OneDrive\Desktop\gambling\.github\workflows\run_daily.yaml) automatically updates the CSV and interactive plot every morning.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you wish to enhance the projections or visualizations.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please reach out to [brianbaldner](https://github.com/brianbaldner).

import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Function to calculate total scores
def calculate_totals(df):
    return df.iloc[:, 1:].sum(axis=1)

# Function to get initials from names
def get_initials(name):
    parts = str(name).split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1][0]}"
    else:
        return str(name)[0] if name else "?"

# Function to get avatar colors
def get_avatar_color(index):
    colors = ["#FF5C8D", "#7B68EE", "#1E90FF", "#32CD32", "#FF8C00", "#9932CC", "#00CED1"]
    return colors[index % len(colors)]

def leaderboard():
    try:
        # Load Excel data - update the path to your Excel file
        file_path = 'marks1.xlsx'
        df = pd.read_excel(file_path)
        
        # Calculate totals and create ranking
        totals = calculate_totals(df)
        
        # Create leaderboard data with ranking
        leaderboard_data = []
        
        # Sort by total scores in descending order
        sorted_indices = totals.sort_values(ascending=False).index
        
        for rank, idx in enumerate(sorted_indices):
            name = df.iloc[idx, 0]  # Username is in the first column
            score = int(totals.iloc[idx])  # Total score
            initials = get_initials(name)
            color = get_avatar_color(rank)
            
            # Simulate improvement points (would be calculated from historical data in production)
            improvement = "+12" if rank > 2 else ""
            
            leaderboard_data.append({
                "rank": rank + 1,
                "name": name,
                "score": score,
                "initials": initials,
                "color": color,
                "improvement": improvement
            })
        
        # Pass data to template
        return render_template('leaderboard.html', leaderboard_data=leaderboard_data)
        
    except Exception as e:
        return f"Error loading data: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
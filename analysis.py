import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

matches=pd.read_csv(r"C:\Users\Jakho\Downloads\archive\matches.csv")
deliveries=pd.read_csv(r"C:\Users\Jakho\Downloads\archive\deliveries.csv")

matches[['team1','team2','toss_winner','winner']]=matches[['team1','team2','toss_winner','winner']].replace({'Royal Challengers Bangalore':'Royal Challengers Bengaluru','Kings XI Punjab':'Punjab Kings','Delhi Daredevils':'Delhi Capitals','Rising Pune Supergiants':'Rising Pune Supergiant'})

# Analysis 1: Top batsmen by total runs
top_batsman=deliveries.groupby(['batter'])['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
top_batsman.columns=['Batsman','Runs Scored']
top_batsman.index.name='Sr No.'
top_batsman.index=top_batsman.index+1
print(top_batsman)

# Analysis 2: Wins per team
total_matches = pd.concat([matches['team1'], matches['team2']]).value_counts()
wins = matches['winner'].value_counts()
win_rate_df = (wins / total_matches * 100).sort_values(ascending=False).reset_index()
win_rate_df.columns = ['Team', 'win_rate']
win_rate_df.index.name ='Sr No.'
win_rate_df.index=win_rate_df.index+1
print(win_rate_df)

fig = plt.figure(figsize=(16, 12))
fig.suptitle('IPL Dashboard (2008–2024)', fontsize=18, fontweight='bold', y=0.98)
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# Chart 1: Top 10 batsmen (bar chart)
ax1 = fig.add_subplot(gs[0, :])  # full top row
colors = plt.cm.YlOrRd(np.linspace(0.4, 0.9, 10))
bars = ax1.barh(top_batsman['Batsman'], top_batsman['Runs Scored'], color=colors)
ax1.set_xlabel('Total Runs')
ax1.set_title('Top 10 IPL Run Scorers (all seasons)')
ax1.invert_yaxis()
for bar, val in zip(bars, top_batsman['Runs Scored']):
    ax1.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f'{int(val):,}', va='center', fontsize=9)

# Chart 2: Team win rates (horizontal bar)
ax2 = fig.add_subplot(gs[1, 0])
win_rate_df_top = win_rate_df.head(8)
ax2.barh(win_rate_df_top['Team'], win_rate_df_top['win_rate'],
         color='steelblue')
ax2.set_xlabel('Win Rate (%)')
ax2.set_title('Team Win Rates')
ax2.invert_yaxis()

plt.savefig('ipl_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("Dashboard saved!")
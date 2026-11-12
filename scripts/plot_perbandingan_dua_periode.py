import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent
project_root = root.parent
data_dir = project_root / 'data' / 'processed'
figures_dir = project_root / 'figures'
figures_dir.mkdir(parents=True, exist_ok=True)

def resolve_source(filename: str) -> Path:
    for candidate in [data_dir / filename, project_root / filename, root / filename]:
        if candidate.exists():
            return candidate
    return data_dir / filename

source = resolve_source('panel_perbandingan_dua_periode_14negara.csv')
out = figures_dir / 'perubahan_belanja_dan_impor_WDI_12negara_lengkap.png'
rows=list(csv.DictReader(source.open(encoding='utf-8-sig')))
rows=[r for r in rows if r['arms_imports_change_pct_only_if_5yr_complete']]
labels={'Australia':'Australia','China':'China','India':'India','Indonesia':'Indonesia','Japan':'Japan','Korea, South':'South Korea','Pakistan':'Pakistan','Philippines':'Philippines','Singapore':'Singapore','Thailand':'Thailand','United States of America':'United States','Viet Nam':'Vietnam'}
fig,ax=plt.subplots(figsize=(10.5,7),dpi=180)
fig.patch.set_facecolor('#fbfcfe'); ax.set_facecolor('#fbfcfe')
for r in rows:
 x=float(r['exp_change_pct']); y=float(r['arms_imports_change_pct_only_if_5yr_complete']); name=r['country']
 hi=name in ('Indonesia','Australia')
 color='#d2643b' if name=='Indonesia' else '#137c8b' if name=='Australia' else '#667085'
 ax.scatter(x,y,s=92 if hi else 54,c=color,edgecolor='white',linewidth=1.1,zorder=3,alpha=.96)
 dx,dy=5,5
 if name in ('China','United States of America'): dy=-13
 if name=='Japan': dy=8
 if name=='India': dy=-12
 if name=='Philippines': dy=8
 if name=='Indonesia': dy=10
 if name=='Australia': dy=-16
 ax.annotate(labels.get(name,name), (x,y), xytext=(dx,dy), textcoords='offset points',fontsize=9.3 if hi else 8.4,weight='bold' if hi else 'normal',color='#202939',zorder=4)
ax.axhline(0,color='#344054',linewidth=1.0,linestyle='--',alpha=.8)
ax.axvline(0,color='#344054',linewidth=1.0,linestyle='--',alpha=.8)
ax.grid(True,color='#d9e0e8',linewidth=.65,alpha=.7,zorder=0)
ax.set_xlabel('Change in mean annual military expenditure, 2016–20 to 2021–25 (%)',fontsize=10.5,labelpad=10)
ax.set_ylabel('Change in WDI arms-import indicator, 5-year total (%)',fontsize=10.5,labelpad=10)
ax.set_title('Military expenditure and the WDI arms-import indicator often moved in different directions',fontsize=13.2,weight='bold',loc='left',pad=18,color='#172b4d')
ax.text(0,1.015,'12 selected countries with complete WDI arms-imports data for both five-year periods',transform=ax.transAxes,fontsize=9.5,color='#475467',va='bottom')
fig.text(.12,.035,'WDI MS.MIL.MPRT.KD, constant 1990 US$, sourced from SIPRI; not raw TIV or transaction price. Within-series percentage changes only; no causal relationship is estimated.',fontsize=8,color='#475467',ha='left')
ax.spines[['top','right']].set_visible(False)
ax.spines[['bottom','left']].set_color('#98a2b3')
ax.tick_params(colors='#344054',labelsize=9)
fig.tight_layout(rect=(.10,.12,.99,.91))
fig.savefig(out,bbox_inches='tight',facecolor=fig.get_facecolor())
print(out)

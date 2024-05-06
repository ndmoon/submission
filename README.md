# Setup environment

conda create --name main-ds python=3.11
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel

# Run Streamlit app
cd dashboard
streamlit run dashboard.py
from geopy.geocoders import Nominatim
import pandas as pd

geolocator = Nominatim(user_agent="my_user_agent")

ibge = pd.read_excel('./RELATORIO_DTB_BRASIL_MUNICIPIO.xls')
dataframe = pd.read_csv('./dados_estacoes.csv')

def getLocation(df):
    if not pd.isna(df['Cord_x']) or not pd.isna(df['Cord_y']):
        return df['Cord_y'], df['Cord_x']
    
    else:
        if not pd.isna(df['CodigoIBGE']):
            code = int(df['CodigoIBGE'])
            nome = ibge[ ibge['Código Município Completo'] == code ]['Nome_Município'].values[0]
        
        else:
            nome = df['Nome']

        city, country = nome, 'Brasil'
        
        loc = geolocator.geocode(city+','+ country)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return np.nan, np.nan


for index, item in dataframe.iterrows():
    dataframe.loc[index, [ 'Cord_y', 'Cord_x' ] ] = getLocation(item)

dataframe.to_csv('./arquivo_corrigido.csv', index=False)

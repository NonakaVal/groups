import streamlit as st
from utils.GoogleSheetManager import GoogleSheetManager, update_worksheet
from streamlit_gsheets import GSheetsConnection
import requests
# import qrcode
import io

st.set_page_config(page_title="collectorsguardian", page_icon="📦", layout='wide')
# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
gs_manager = GoogleSheetManager()

# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
def shorten_url_with_requests(url, timeout=10):
    
    api_url = f"http://tinyurl.com/api-create.php?url={url}"
    try:
        response = requests.get(api_url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Erro ao encurtar a URL: {str(e)}"
# def generate_qr_code(link):
#     qr_img = qrcode.make(link)
#     buffer = io.BytesIO()
#     qr_img.save(buffer, format="PNG")
#     buffer.seek(0)
#     return buffer
# # Função para encurtar todos os links no DataFrame
def shorten_links_in_df(df, link_column="URL"):
    df[link_column] = df[link_column].apply(lambda x: shorten_url_with_requests(x))
    return df
# URL da planilha Google Sheets
url = st.secrets["url"]

def norm(data):

    data['SENT'] = data['SENT'].astype(bool)
    return data

if url:
    gs_manager.set_url(url)
    gs_manager.add_worksheet(url, "PRIME")
    gs_manager.add_worksheet(url, "ESSENCIALS")
    gs_manager.add_worksheet(url, "LEILÕES")   
    prime = gs_manager.read_sheet(url, "PRIME")
    prime = norm(prime)
    essencials = gs_manager.read_sheet(url, "ESSENCIALS")
    essencials = norm(essencials)
    leiloes = gs_manager.read_sheet(url, "LEILÕES")
    leiloes = norm(leiloes)

# Preparando os dados

def get_link(data):
    data['URL'] = data.apply(lambda row: f"https://www.collectorsguardian.com.br/{row['ITEM_ID'][:3]}-{row['ITEM_ID'][3:]}-{row['TITLE'].replace(' ', '-').lower()}-_JM#item_id={row['ITEM_ID']}", axis=1)
    data = data[['ITEM_ID', 'TITLE', 'URL', "DATA",  'SENT' ]]

    data = shorten_links_in_df(data)
    return data

# prime = get_link(prime)

# essencials = get_link(essencials)

st.subheader("PRIME")

# st.dataframe(prime, column_config={"URL": st.column_config.LinkColumn("Links", display_text="Acessar anúncio")})
prime = st.data_editor(prime)
update_worksheet(prime, "PRIME", 5, url)



# # Gerando os QR Codes e exibindo no Streamlit
# st.subheader("QR Codes para os Links Encurtados")
# for index, row in prime.iterrows():
#     st.write(f"Item: {row['TITLE']}")
#     st.write(f"Link encurtado: {row['URL']}")
    
#     # Gerando QR Code
#     qr_code_img = generate_qr_code(row['URL'])
    
#     # Exibindo a imagem do QR Code
#     st.image(qr_code_img, caption=row['TITLE'], use_column_width=False)



st.subheader("ESSENCIALS")
# st.dataframe(essencials, column_config={"URL": st.column_config.LinkColumn("Links", display_text="Acessar anúncio")})
# # st.dataframe(prime, column_config={"URL": st.column_config.LinkColumn("Links", display_text="Acessar anúncio")})

essencials= st.data_editor(essencials)
update_worksheet(essencials, "ESSENCIALS", 100,url)
# # Gerando os QR Codes e exibindo no Streamlit
# st.subheader("QR Codes para os Links Encurtados")
# for index, row in essencials.iterrows():
#     st.write(f"Item: {row['TITLE']}")
#     st.write(f"Link encurtado: {row['URL']}")
    
#     # Gerando QR Code
#     qr_code_img = generate_qr_code(row['URL'])

#     # Exibindo a imagem do QR Code
#     st.image(qr_code_img, caption=row['TITLE'], use_column_width=False)


st.subheader("LEILÕES")

# st.dataframe(leiloes, column_config={"URL": st.column_config.LinkColumn("Links", display_text="Acessar anúncio")})
leiloes = st.data_editor(leiloes)

update_worksheet(leiloes, "LEILÕES", 6, url)
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Gestión de Entregas", layout="wide")
st.title("🚚 Sistema de Gestión de Pedidos")

# 1. Definimos nombres de columnas estándar (sin tildes para evitar errores)
COL_CLIENTES = ['ID', 'Nombre', 'Direccion']
COL_PEDIDOS = ['Cliente_ID', 'Producto', 'Estado']

# 2. Crear archivos si no existen
if not os.path.exists('clientes.csv'):
    pd.DataFrame(columns=COL_CLIENTES).to_csv('clientes.csv', index=False)
if not os.path.exists('pedidos.csv'):
    pd.DataFrame(columns=COL_PEDIDOS).to_csv('pedidos.csv', index=False)

# 3. Leer datos
df_clientes = pd.read_csv('clientes.csv')
df_pedidos = pd.read_csv('pedidos.csv')

menu = ["Ver Entregas", "Añadir Cliente", "Nuevo Pedido"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "Ver Entregas":
    st.subheader("📋 Pedidos Actuales")
    if not df_pedidos.empty and not df_clientes.empty:
        # Relacionamos las tablas
        resultado = pd.merge(df_clientes, df_pedidos, left_on='ID', right_on='Cliente_ID')
        # Mostramos solo las columnas que existen seguro
        st.table(resultado[['Nombre', 'Direccion', 'Producto', 'Estado']])
    else:
        st.info("No hay datos suficientes para mostrar entregas. Registra un cliente y un pedido.")

elif choice == "Añadir Cliente":
    st.subheader("👤 Nuevo Cliente")
    with st.form("f_cli"):
        id_c = st.number_input("ID", min_value=1)
        nom = st.text_input("Nombre")
        dir_cli = st.text_input("Dirección")
        if st.form_submit_button("Guardar"):
            nuevo = pd.DataFrame([[id_c, nom, dir_cli]], columns=COL_CLIENTES)
            nuevo.to_csv('clientes.csv', mode='a', header=False, index=False)
            st.success("Guardado. Recarga la página.")
            st.rerun()

elif choice == "Nuevo Pedido":
    st.subheader("📦 Nuevo Pedido")
    if not df_clientes.empty:
        with st.form("f_ped"):
            c_nom = st.selectbox("Cliente", df_clientes['Nombre'])
            id_sel = df_clientes[df_clientes['Nombre'] == c_nom]['ID'].values[0]
            prod = st.text_input("Producto")
            if st.form_submit_button("Registrar"):
                nuevo_p = pd.DataFrame([[id_sel, prod, "Pendiente"]], columns=COL_PEDIDOS)
                nuevo_p.to_csv('pedidos.csv', mode='a', header=False, index=False)
                st.success("Pedido anotado")
                st.rerun()
    else:
        st.error("Registra un cliente primero.")
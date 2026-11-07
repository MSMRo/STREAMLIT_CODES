import pandas as pd
import streamlit as st

st.title("Proyecto del curso TADTIS")
st.write(
    """
    Presentación de mis proyecto \n 
    Se muestra aqui:
    """
)

### Gráficas en streamlit

data = {
    "t": [23,45,67,65,34,23,45],
    "h": [45,67,23,44,55,66,77]
}

df = pd.DataFrame(data)

st.line_chart(df)


### Agregar un boton
if st.button("Click me!!"):
    st.write("Prendido")
elif st.button("Apagar"):
    st.write("Apagado")
import streamlit as st
import pandas as pd

# --------------------------
# PANTALLA DE BIENVENIDA
# --------------------------
st.title("🥗 Tu Asistente de Dietas Personalizadas")
st.markdown("""
¡Bienvenido! 🎉  
Esta aplicación te ayudará a estimar la evolución de tu peso y a obtener un plan semanal de dieta **de manera orientativa**.  

⚠️ **Aviso importante:** Cada persona es distinta. Esta app no reemplaza la asesoría de un **profesional de la salud o nutrición**.
""")

st.divider()

# --------------------------
# FORMULARIO DE USUARIO
# --------------------------
st.header("📋 Datos del usuario")

with st.form("user_form"):
    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", min_value=10, max_value=100, step=1)
    peso_actual = st.number_input("Peso actual (kg)", min_value=30.0, max_value=200.0, step=0.1)
    altura = st.number_input("Altura (cm)", min_value=120, max_value=220, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
    actividad = st.selectbox("Nivel de actividad", ["Sedentario", "Ligero", "Moderado", "Activo", "Muy activo"])
    objetivo = st.selectbox("Objetivo", ["Bajar peso", "Mantener peso", "Subir peso"])

    submitted = st.form_submit_button("Calcular mi plan")

# --------------------------
# PROCESAMIENTO
# --------------------------
if submitted:
    st.success(f"✅ Gracias {nombre}, aquí tienes tu plan personalizado:")

    # Calorías de mantenimiento (fórmula simplificada Harris-Benedict)
    if sexo == "Masculino":
        tmb = 88.36 + (13.4 * peso_actual) + (4.8 * altura) - (5.7 * edad)
    else:
        tmb = 447.6 + (9.2 * peso_actual) + (3.1 * altura) - (4.3 * edad)

    factores = {
        "Sedentario": 1.2,
        "Ligero": 1.375,
        "Moderado": 1.55,
        "Activo": 1.725,
        "Muy activo": 1.9
    }
    calorias_mantenimiento = tmb * factores[actividad]

    # Ajuste según objetivo
    if objetivo == "Bajar peso":
        calorias_objetivo = calorias_mantenimiento - 500
    elif objetivo == "Subir peso":
        calorias_objetivo = calorias_mantenimiento + 500
    else:
        calorias_objetivo = calorias_mantenimiento

    st.metric("Calorías diarias recomendadas", f"{calorias_objetivo:.0f} kcal")

    # Simulación de evolución de peso (4 semanas)
    if objetivo == "Bajar peso":
        perdida_semana = 0.5
        proyeccion = [peso_actual - i * perdida_semana for i in range(5)]
    elif objetivo == "Subir peso":
        ganancia_semana = 0.5
        proyeccion = [peso_actual + i * ganancia_semana for i in range(5)]
    else:
        proyeccion = [peso_actual for _ in range(5)]

    semanas = ["Semana 0", "Semana 1", "Semana 2", "Semana 3", "Semana 4"]
    df_progreso = pd.DataFrame({"Semana": semanas, "Peso estimado (kg)": proyeccion})

    st.subheader("📊 Evolución estimada de tu peso")
    st.dataframe(df_progreso, hide_index=True)

    # --------------------------
    # DIETA SEMANAL CON GRAMOS
    # --------------------------
    st.subheader("🍽️ Dieta semanal sugerida con cantidades (ejemplo)")
    
    dieta = pd.DataFrame({
        "Día": [
            "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
        ],
        "Desayuno": [
            "50 g avena + 200 ml leche + 1 banano",
            "2 huevos + 40 g pan integral + 1 naranja",
            "200 g yogurt natural + 30 g granola + 1 manzana",
            "40 g pan integral + 30 g queso fresco + 1 huevo",
            "2 tostadas + 50 g aguacate + 1 taza café",
            "2 huevos revueltos + 30 g espinaca + 1 arepa pequeña",
            "250 ml batido verde (espinaca, piña, pepino)"
        ],
        "Almuerzo": [
            "150 g pollo a la plancha + 80 g arroz + 100 g brócoli",
            "150 g carne magra + 120 g ensalada variada",
            "120 g pasta integral + 100 g pechuga de pollo",
            "150 g pescado + 100 g verduras al vapor + 70 g papa",
            "150 g pollo al horno + 100 g ensalada fresca",
            "100 g arroz + 2 huevos + 50 g tomate",
            "200 g sopa de verduras + 1 arepa pequeña"
        ],
        "Cena": [
            "100 g atún + 150 g ensalada verde",
            "200 g sopa de pollo + 30 g pan integral",
            "150 g ensalada variada + 50 g pechuga",
            "120 g pechuga a la plancha + 100 g ensalada",
            "1 wrap integral (80 g tortilla + pollo + verduras)",
            "200 g ensalada fresca + 30 g queso",
            "120 g pescado al vapor + 100 g ensalada"
        ]
    })

    st.dataframe(dieta, hide_index=True)

    # Descargar CSV
    csv = dieta.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar mi dieta semanal",
        data=csv,
        file_name="mi_dieta.csv",
        mime="text/csv"
    )



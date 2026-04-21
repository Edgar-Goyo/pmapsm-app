# 🌿 Guía de Aplicabilidad PMA-PSM
### Oleoducto de los Llanos Orientales · Bicentenario · HSE-G-008 v6

Aplicación web para consultar, filtrar y generar reportes de aplicabilidad del **Plan de Manejo Ambiental (PMA)** y **Plan de Seguimiento y Monitoreo (PSM)** para contratos ODL y OBC.

---

## ✨ Funcionalidades

| Módulo | Descripción |
|--------|-------------|
| 🔎 **Buscador** | Búsqueda tipo Google por palabras clave del contrato |
| 📊 **Dashboard** | Gráficas de aplicabilidad por familia y fichas |
| 📁 **Cargar archivo** | Sube nueva versión del Excel `.xlsm` |
| 📑 **Ficha de proyecto** | Perfil completo PMA/PSM + exportar reporte |

---

## 🚀 Despliegue en Streamlit Cloud (recomendado)

1. Haz **fork** de este repositorio en tu cuenta GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub
4. Selecciona este repositorio → rama `main` → archivo `app.py`
5. Clic en **Deploy** → en ~2 minutos tienes tu URL

---

## 💻 Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/pmapsm-app.git
cd pmapsm-app

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run app.py
```

La app abre en: **http://localhost:8501**

---

## 📁 Estructura del proyecto

```
pmapsm-app/
├── app.py                  # App principal Streamlit
├── requirements.txt        # Dependencias Python
├── .streamlit/
│   └── config.toml         # Tema corporativo verde
├── data_odl_clean.csv      # Datos limpios ODL (410 registros)
├── data_obc_clean.csv      # Datos limpios OBC (310 registros)
├── fichas_meta.csv         # Descripción de las 51 fichas PMA-PSM
└── .gitignore
```

---

## 🔄 Actualizar los datos

Para actualizar cuando hay una nueva versión del Excel:

1. Abre la app → módulo **📁 Cargar archivo**
2. Sube el nuevo `.xlsm`
3. Haz clic en **Procesar y actualizar datos**
4. Los CSV se actualizan automáticamente

O manualmente:
```bash
# Reemplaza los CSV y haz commit
git add data_odl_clean.csv data_obc_clean.csv
git commit -m "Actualización datos PMA-PSM - [fecha]"
git push
```

Streamlit Cloud redespliega automáticamente con cada `git push`.

---

## 📬 Contacto

- **Profesional Ambiental Sr.:** sonia.frayle@odl.com.co  
- **Profesional ICAS:** derly.neira@odl.com.co

---

## 🗺️ Roadmap

- [x] Fase 1 — Buscador + Dashboard + Ficha de proyecto
- [ ] Fase 2 — Login por roles (ambiental / contratista / revisor)
- [ ] Fase 3 — Mapa interactivo estaciones ODL/OBC
- [ ] Fase 4 — Envío automático de reportes por correo

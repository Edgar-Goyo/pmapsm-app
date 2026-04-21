# 📋 GUÍA: Subir la app a GitHub y publicar en Streamlit Cloud
## Guía Aplicabilidad PMA-PSM · ODL / Bicentenario

---

## PASO 1 — Crear cuenta en GitHub (si no tienes)
1. Ve a https://github.com/signup
2. Crea cuenta con tu correo corporativo ODL
3. Verifica el correo

---

## PASO 2 — Crear el repositorio en GitHub
1. Inicia sesión en https://github.com
2. Clic en el botón verde **"New"** (esquina superior izquierda)
3. Configura el repositorio:
   - **Repository name:** `pmapsm-app`
   - **Description:** Guía de Aplicabilidad PMA-PSM ODL Bicentenario
   - **Visibility:** Private ✅ (recomendado para datos internos)
   - ✅ Marca "Add a README file"
4. Clic en **"Create repository"**

---

## PASO 3 — Subir los archivos al repositorio

### Opción A — Desde el navegador (sin instalar nada)
1. Entra a tu repositorio en GitHub
2. Clic en **"Add file"** → **"Upload files"**
3. Arrastra TODOS estos archivos:
   ```
   app.py
   requirements.txt
   data_odl_clean.csv
   data_obc_clean.csv
   fichas_meta.csv
   generar_datos.py
   .gitignore
   ```
4. En el mensaje escribe: `Versión inicial app PMA-PSM`
5. Clic en **"Commit changes"**

6. Ahora sube la carpeta `.streamlit`:
   - Clic en **"Add file"** → **"Create new file"**
   - En el nombre escribe: `.streamlit/config.toml`
   - Pega el contenido del archivo `config.toml`
   - Clic en **"Commit new file"**

### Opción B — Desde la terminal (con Git instalado)
```bash
# Clonar el repo vacío
git clone https://github.com/TU_USUARIO/pmapsm-app.git
cd pmapsm-app

# Copiar todos los archivos aquí
# (pega los archivos en esta carpeta)

# Subir todo
git add .
git commit -m "Versión inicial app PMA-PSM"
git push origin main
```

---

## PASO 4 — Publicar en Streamlit Cloud

1. Ve a https://share.streamlit.io
2. Clic en **"Sign in with GitHub"**
3. Autoriza a Streamlit a acceder a tus repositorios
4. Clic en **"New app"**
5. Configura:
   - **Repository:** `TU_USUARIO/pmapsm-app`
   - **Branch:** `main`
   - **Main file path:** `app.py`
6. Clic en **"Deploy!"**
7. Espera ~2 minutos mientras se instalan las dependencias
8. ¡Tu app estará disponible en una URL como:
   `https://pmapsm-app-odl.streamlit.app`

---

## PASO 5 — Compartir el enlace

Puedes compartir la URL con:
- ✅ Funcionarios internos ODL/BIC
- ✅ Contratistas externos
- ✅ Por correo, WhatsApp, Teams, etc.
- ✅ Sin necesidad de instalar nada

---

## 🔄 Actualizar la app en el futuro

Cuando tengas una nueva versión del Excel:

```bash
# Opción A: Usar el script automático
python generar_datos.py nueva_guia.xlsm

# Opción B: Desde la app (módulo "Cargar archivo")
# Sube el xlsm → procesar → los CSV se actualizan

# Luego subir a GitHub
git add data_odl_clean.csv data_obc_clean.csv
git commit -m "Actualización datos - [fecha]"
git push
```

Streamlit Cloud detecta el push y **redespliega automáticamente** en ~1 minuto.

---

## ❓ Problemas frecuentes

| Problema | Solución |
|----------|----------|
| Error al hacer deploy | Verifica que `requirements.txt` esté en la raíz del repo |
| La app no carga los datos | Verifica que los 3 CSV estén subidos al repo |
| Error de módulo no encontrado | Espera que Streamlit instale las dependencias (~3 min) |
| Quiero cambiar el tema de color | Edita `.streamlit/config.toml` |

---

## 📬 Soporte
- Profesional Ambiental: sonia.frayle@odl.com.co
- Profesional ICAS: derly.neira@odl.com.co

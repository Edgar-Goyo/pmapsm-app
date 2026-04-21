"""
Genera los archivos CSV limpios a partir del Excel GUIA_APLICABILIDAD_PMAPSM.xlsm
Uso: python generar_datos.py ruta/al/archivo.xlsm
"""
import sys
import pandas as pd
import numpy as np


def limpiar_hoja(df_raw, ficha_row=8, data_start=11):
    fichas = [str(x).strip() for x in df_raw.iloc[ficha_row, 4:].tolist()]
    data = df_raw.iloc[data_start:].copy()
    data.columns = ['FAMILIA', 'OBJETO_ALCANCE', 'SI', 'NO'] + fichas
    data = data.reset_index(drop=True)

    data['FAMILIA'] = data['FAMILIA'].replace('nan', np.nan)
    data['FAMILIA'] = data['FAMILIA'].apply(
        lambda x: str(x).replace('|', '').strip() if pd.notna(x) else np.nan
    )
    data['FAMILIA'] = data['FAMILIA'].ffill()

    data = data[
        data['OBJETO_ALCANCE'].notna() &
        (data['OBJETO_ALCANCE'].astype(str).str.strip() != 'nan')
    ]

    data['APLICA_PMA_PSM'] = data['SI'].apply(
        lambda x: True if str(x).strip().upper() == 'SI' else False
    )
    for col in fichas:
        data[col] = data[col].apply(
            lambda x: True if str(x).strip().upper() == 'X' else False
        )
    data = data.drop(columns=['SI', 'NO'])

    def get_fichas_list(row):
        return [f for f in fichas if row.get(f, False)]

    data['FICHAS_APLICAN'] = data.apply(get_fichas_list, axis=1)
    data['NUM_FICHAS'] = data['FICHAS_APLICAN'].apply(len)
    return data, fichas


def main(ruta_excel):
    print(f"📂 Leyendo: {ruta_excel}")

    # Detectar hojas
    xl = pd.ExcelFile(ruta_excel, engine='openpyxl')
    hojas = xl.sheet_names
    print(f"   Hojas encontradas: {len(hojas)}")

    hoja_odl = next((h for h in hojas if 'ODL' in h.upper() or 'LÍNEA' in h.upper() or 'LINEA' in h.upper()), None)
    hoja_obc = next((h for h in hojas if 'OBC' in h.upper() or 'BIC' in h.upper()), None)

    if not hoja_odl:
        print("⚠️  No se encontró hoja ODL. Selecciona manualmente:")
        for i, h in enumerate(hojas[:10]):
            print(f"   {i}: {h}")
        idx = int(input("Índice hoja ODL: "))
        hoja_odl = hojas[idx]

    if not hoja_obc:
        print("⚠️  No se encontró hoja OBC/BIC. Selecciona manualmente:")
        for i, h in enumerate(hojas[:10]):
            print(f"   {i}: {h}")
        idx = int(input("Índice hoja OBC: "))
        hoja_obc = hojas[idx]

    print(f"   ODL → '{hoja_odl}'")
    print(f"   OBC → '{hoja_obc}'")

    # Procesar ODL
    df_odl_raw = pd.read_excel(ruta_excel, sheet_name=hoja_odl, header=None, engine='openpyxl')
    odl, fichas_odl = limpiar_hoja(df_odl_raw)
    odl.to_csv('data_odl_clean.csv', index=False)
    print(f"✅ data_odl_clean.csv — {len(odl)} registros, {odl['FAMILIA'].nunique()} familias")

    # Procesar OBC
    df_obc_raw = pd.read_excel(ruta_excel, sheet_name=hoja_obc, header=None, engine='openpyxl')
    obc, fichas_obc = limpiar_hoja(df_obc_raw)
    obc.to_csv('data_obc_clean.csv', index=False)
    print(f"✅ data_obc_clean.csv — {len(obc)} registros, {obc['FAMILIA'].nunique()} familias")

    # Metadata fichas (usar ODL como referencia)
    desc_row = df_odl_raw.iloc[10, 4:].tolist()
    meta = pd.DataFrame({'FICHA': fichas_odl, 'DESCRIPCION': [str(d).strip() for d in desc_row]})
    meta.to_csv('fichas_meta.csv', index=False)
    print(f"✅ fichas_meta.csv — {len(meta)} fichas")
    print("\n🎉 ¡Datos actualizados! Haz git push para reflejar cambios en la app.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python generar_datos.py ruta/al/archivo.xlsm")
        sys.exit(1)
    main(sys.argv[1])

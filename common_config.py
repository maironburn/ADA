#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# to fake integration
CORE_DIR = os.path.join(ROOT_DIR, "core")
ML = os.path.join(CORE_DIR, "ml")
SVM = os.path.join(ML, "SVM")

SETTINGS = os.path.join(SVM, 'settings')
EXTRACCION_IT = os.path.join(SVM, "averias_train_all_to_coremain{}{}".format(os.path.sep,
                                                                             "averias_train_all_to_coremain.csv"))

MODELS_DEST_FOLDER = os.path.join(SVM, "data_file_model")
MLP_JOBLIB = os.path.join(SVM, "data_file_model{}{}.pkl".format(os.path.sep, "mlp_model"))
TF_IDF = os.path.join(SVM, "data_file_model{}{}.joblib".format(os.path.sep, "tf_idf"))
JSON_ID_CAT = os.path.join(SVM, "data_file_model{}{}.json".format(os.path.sep, "json_id_cat"))

data = [{
    'detalle': 'Cliente con  instancia(pago aplazado, descuentos..) con fecha fin en smart y con fecha fin posterior en geneva.',
    'case_history': """*** CREACION 02/08/2019 05:50:23 jpalomio [SAC_Especializado] [GT: Reclam BO Vall] Action Type: Incoming call. Comentarios: # TTPP CADIZ # Remitente : Laura Correas <laura.correas@smobile.es>Enviado : miércoles, 31 de julio de 2019 14:53 Para : HR_Particular@vodafone.es <HR_Particular@vodafone.es>Asunto : Fwd: HOJA RECLAMACION[Case: 000R7aEJWMEYP0X7- 00] ---------------------------------------------------- - NOTAS DE CORREO : se adjunta hoja de reclamacion  ------------------------------------------------------ - RUTA DE DOCUMENTOS GUARDADOS EN : J:\INF\Inf_Consumo_SATISFACCION_CARTAS\5. VALLADOLID\10.ADJUNTOS  E-GAIN\2019\TERCER TRIMESTRE\AGOSTO\02 AGOSTO\HR-Villanego Fernandez,Maria Del Rosario-84087805""",
    'case_type_lvl1': 'Hoja Reclamaciones',
    'case_type_lvl2': '',
    'case_type_lvl3': '',
    'oper_system': 'Disconforme abono',
    's_title': 'FACTURA',
    'x_codigo_apertura': 'Factura',
    'x_grupo_trabajo': 'Reclam BO Vall',
    'x_sistema_afectado': '',
    'x_tipo_2': '',
    'x_tipo_3': ''
}]

# cron_email_facturas

descarga facturas electronicas de colombia del correo electronico

## contexto

en colombia las facturas electronicas se mandan por correo electronico, para automatizar la recolección y catalogo de las mismas se crea un script que las analiza y las cataloga por año, tambien permite borrar documentos html falsos positivos y borrar los attatchments de los mismos que no sean necesarios

## uso
- instala thunderbird y configura tu cuenta de gmail
- instala el plugin [ImportExportTools NG](https://addons.thunderbird.net/es/thunderbird/addon/importexporttools-ng/) para poder exportar los correos a archivos
- filtra tus correos para que te muestre los correos que tengan la palabra factura en la descripcion, el remitente o el contenido
- selecctiona tus correos y da click derecho en los correos seleccionados, en el menu que sale da click en "guardar los mensajes seleccionados" y a continuacion click en "Formato HTML (with attatchments)"
- seleccionar una carpeta en la que guardar los correos exportados
- ejecutar este proyecto dando como entrada la carpeta en la que se exportaron los correos

## trabajo futuro

- poder diferenciar automaticamente facturas electrónicas de falsos positivos
- hacer un index o un excel para ayudar al contador a procesar las facturas teniendo el numero de la factura, el precio y el generador de la factura
- poder descargar los correos electrónicos desde gmail sin usar thunderbird
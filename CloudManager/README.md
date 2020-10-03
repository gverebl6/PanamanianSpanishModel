# Cloud Manager Module

Se encarga del manejo de los Storage de GCP donde se guardan los archivos. 

Este modulo se utiliza intanciado en otros modulos para poder hacer la descarga  y subida de los archivos. 

Cosas que hay que tomar en cuenta es que para que este funcione se tiene que agregar una llave de cuenta de servicio de GCP con el comando 

```
export GOOGLE_APPLICATION_CREDENTIAL=ruta/de/la/llave
``` 

# Microservicio Estaciones Meteorológicas HomeSoul conectadas a FIWARE
Este microservicio permite a los usuarios conectarse a una red de estaciones meteorológicas HomeSoul y acceder a los datos meteorológicos en tiempo real a través de la plataforma FIWARE.

## Características:

- Estaciones meteorológicas HomeSoul equipadas con sensores de alta precisión que miden variables como la temperatura, la humedad, la presión atmosférica y la velocidad del viento.
- Datos recolectados son enviados a través de una conexión inalámbrica a un servidor central que los procesa y los expone a través de una interfaz de programación de aplicaciones (API) utilizando el estándar de protocolo FIWARE.
- Acceso a los datos meteorológicos a través de la herramienta Grafana.
- Conectando a FIWARE, los datos meteorológicos recolectados pueden ser combinados con otros datos de sensores y utilizados para aplicaciones de automatización y toma de decisiones en tiempo real.

## Instrucciones despliegue usando DOCKER
Usar  `docker-compose`.

## To Do
Usar secrets en variables de entorno.
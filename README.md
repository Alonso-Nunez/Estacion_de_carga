# Estacion_de_carga

Repositorio creado con el propósito de hacer el código del proyecto TT2023-B044

### Rama de la rasp

##### Pines de conexión:
|Pin GPIO|Pin Físico|Uso|
|:--:|:--:|:--:|
|5|29|Switch bateria|
|6|31|Switch inversor|
|12|32|Activador por interruptor|
|22|15|Switch CFE|
|23|16|Switch Panel Solar|
|24|18|Switch Aerogenerador|
|25|22|Pulso PWM|

### Variables del entorno virtual

Instruccion para crear el entorno

```
python -m venv env
```

Instruccion para activar el entorno

```
env/scripts/activate
```

Librerias a instalar
django

```
pip install django
```

djongo

```
pip install djongo
```

Instalar env para funcion de vistas
``` 
pip install django-environ
```
Instalar pymongo paara extrare datos de MongoDB
``` 
pip install pymongo
```

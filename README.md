```
  ███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗     usage: sphish.py [-h] [-c] [-n NGROK] [-s SMS] [-a ALL]
  ██╔════╝██╔══██╗██║  ██║██║██╔════╝██║  ██║
  ███████╗██████╔╝███████║██║███████╗███████║     optional arguments:
  ╚════██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║      -n NGROK, --ngrok NGROK
  ███████║██║     ██║  ██║██║███████║██║  ██║	   -c, --check           check and install dependencies
  ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝	   -a ALL, --all ALL     Smishing with Ngrok
	 		Created by WackyH4cker
```

**Sphish** es una excelente herramienta de *Smishing* dedicada a la simulación de campañas de *Phishing* mediante envíos masivos de **SMS**.

Permite la elección de una plantilla personalizada, además del levantamiento de esta mediante **Ngrok**.

También incluye:

- Mensaje personalizado
- Suplantación de identidad
### Instalación
```
git clone https://github.com/wackyhacker/Sphish
```
```
cd Sphish
```
```
pip3 install -r requeriments.txt
```
```
chmod +x sphish.py
```
```
./sphish.py --help
```
Asignar *Service Plan ID* de [SinchSMS](https://sinchsms.com) en esta seccion de codigo.
```
sphish = Sphish('ngrok', getoutput('whoami'), '<ID>') # <- Enter your Service Plan ID
```

### Usó

```
./sphish.py --help # Panel de ayuda
./sphish.py --check # Verificar e instalar dependencias necesarias
./sphish.py --ngrok <authtoken> # Instalar ngrok y asignar el authtoken
./sphish.py --all <secret_key> # Iniciar la herramienta asignando clave secreta
```


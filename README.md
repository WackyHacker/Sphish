```
███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗     usage: sphish.py [-h] [-c] [-n NGROK] [-s SMS] [-a ALL]
██╔════╝██╔══██╗██║  ██║██║██╔════╝██║  ██║
███████╗██████╔╝███████║██║███████╗███████║     optional arguments:
╚════██║██╔═══╝ ██╔══██║██║╚════██║██╔══██║        -n NGROK, --ngrok NGROK
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
cd Sphish & pip3 install -r requeriments.txt
```
```
chmod +x sphish.py
```
```
./sphish.py --help
```
### Usó
Para el uso correcto de esta herramienta se requieren una serie de dependencias:
- PHP
- wget

Use el parámetro `--check` para su instalación, este verificara si existen, de lo contrario las instalara. 

<p align="center"><img src="https://user-images.githubusercontent.com/69093629/163915016-5f745465-c8a7-489a-a1ac-3586c25bc48f.png"/></p>




# Minha API

Este pequeno projeto faz parte do material diático das aulas de  **Bootcamp Full Stack** 

O objetivo aqui é ilutsrar o conteúdo apresentado ao longo das aulas.

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://packaging.python.org/pt_BR/latest/guides/installing-using-pip-and-virtual-environments/).

Se estiver utilizando sistema operacional Unix/macOS, executar os seguintes comandos. Caso estiver utilizando Windows, consultar os comandos equivalentes em [comandos_virtualenv](https://packaging.python.org/pt_BR/latest/guides/installing-using-pip-and-virtual-environments/):

```
(env)$ pip install -r requirements.txt

or 

(env)$ pip3 install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.